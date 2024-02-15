from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Thread, Group, GroupMessage, ChatMessage
from itertools import chain
from django.db.models import Value, BooleanField
from django.views.decorators.http import require_POST




User = get_user_model()


@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    groups = Group.objects.filter(members=request.user).prefetch_related('groupmessage_group').order_by('created_at')

    threads = threads.annotate(is_thread=Value(True, output_field=BooleanField()))
    groups = groups.annotate(is_group=Value(True, output_field=BooleanField()))

# Combining threads and groups

    threads_and_groups = list(chain(threads, groups))

    context = {
        'threads': threads,
        'groups':groups,
        'threads_and_groups':threads_and_groups,
    }
    return render(request, 'chat/messages.html',context)





@login_required
def search_users(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id).values('id', 'username')
    return JsonResponse(list(users), safe=False)



@login_required
def create_thread(request):
    selected_user_id = request.POST.get('selected_user_id')
    selected_user = User.objects.get(id=selected_user_id)
    thread, created = Thread.objects.get_or_create(
        first_person=request.user, 
        second_person=selected_user
    )
    chat_url = '/chat/'
    return JsonResponse({'unique_id': str(thread.unique_id), 'created': created, 'redirect_url': chat_url})





# In your views.py

@login_required
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if group_name:
            # Create the group and add the user
            group = Group.objects.create(name=group_name)
            group.members.add(request.user)
            chat_url = '/chat/'
            return JsonResponse({'group_unique_id': group.unique_id,'redirect_url': chat_url})
        else:
            return JsonResponse({'error': 'Invalid group name'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    



@login_required
def search_users_add_to_group(request, group_unique_id):
    query = request.GET.get('query', '')
    group = Group.objects.get(unique_id=group_unique_id)

    # group_data = model_to_dict(group, fields=['id', 'name', 'unique_id'])

    users = User.objects.filter(username__icontains=query).exclude(id__in=group.members.all()).values('id', 'username')
    return JsonResponse(list(users) ,safe=False)


@login_required
def add_to_group(request):
    selected_user_id = request.POST.get('selected_user_id')
    selected_group_unique_id = request.POST.get('selected_group_unique_id')

    group = Group.objects.get(unique_id=selected_group_unique_id)
    user = User.objects.get(id=selected_user_id)

    group.members.add(user)

    chat_url = '/chat/'
    return JsonResponse({'redirect_url': chat_url})





@login_required
def mark_messages_as_read(request):
    unique_id = request.POST.get('unique_id')
    user = request.user

    thread = Thread.objects.filter(unique_id=unique_id).first()
    if thread:
        if user == thread.first_person or user == thread.second_person:
            ChatMessage.objects.filter(thread=thread, is_read=False).update(is_read=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'User not part of the thread'}, status=403)


    group = Group.objects.filter(unique_id=unique_id).first()
    if group:
        if group.members.filter(id=user.id).exists():
            GroupMessage.objects.filter(group=group, is_read=False).update(is_read=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'User not part of the group'}, status=403)

    return JsonResponse({'error': 'Thread or group not found'}, status=404)



@login_required
def mark_messages_as_read_for_ongoing_chat(request):
    unique_id = request.POST.get('unique_id')
    user = request.user

    thread = Thread.objects.filter(unique_id=unique_id).first()
    if thread:
        if user == thread.first_person or user == thread.second_person:
            ChatMessage.objects.filter(thread=thread, is_read=False).update(is_read=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'User not part of the thread'}, status=403)


    group = Group.objects.filter(unique_id=unique_id).first()
    if group:
        if group.members.filter(id=user.id).exists():
            GroupMessage.objects.filter(group=group, is_read=False).update(is_read=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'User not part of the group'}, status=403)

    return JsonResponse({'error': 'Thread or group not found'}, status=404)


