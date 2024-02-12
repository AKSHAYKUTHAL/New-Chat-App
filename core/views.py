from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages,auth
from django.contrib.auth import get_user_model

User = get_user_model()


# from .forms import SignUpForm

def frontpage(request):
    return render(request, 'core/frontpage.html')




def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in.')
        return redirect('messages_page')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            if not user.is_registered:
                request.session['user_id_for_password'] = user.id
                return redirect('create_new_password')
            else:
                auth.login(request,user)
                messages.success(request, 'You are now logged in.')
                return redirect('messages_page')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')
    
    return render(request,'core/login.html')



def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')


def create_new_password(request):
    if request.method == 'POST':
        new_pass = request.POST['new_password']
        confirm_pass = request.POST['confirm_password']
        user_id = request.session.get('user_id_for_password')

        if user_id and new_pass == confirm_pass:
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_pass)
                user.is_registered = True
                user.save()
                messages.success(request, 'Created new password successfully.')
                del request.session['user_id_for_password']
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'An error occurred. Please try again.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match or session expired.')
            return render(request, 'core/create_new_password.html')


    if 'user_id_for_password' not in request.session:
        return redirect('login')

    return render(request, 'core/create_new_password.html')