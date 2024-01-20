from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Thread,User




@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html',context)





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
    return JsonResponse({'thread_id': thread.id,'unique_id': str(thread.unique_id), 'created': created, 'redirect_url': chat_url})