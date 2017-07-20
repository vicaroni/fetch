from django.shortcuts import render, redirect
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserForm, RegisterForm
from .models import UserRepository, DeployKey

# Create your views here.
@login_required
def key_list(request, response):
    if response == 'update':
        result = call_command('key_download', request.user.username, request.user.tokens.first().token)
        if result == 'not_found':
            return render(request, 'fetch/key_list.html', {'user': request.user, 'error': 'Token not found on Github'})
    return render(request, 'fetch/key_list.html', {'user': request.user})

@login_required
def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            token = form.save(commit=False)
            token.user = request.user
            token.save()
            return redirect('key_list', response='')
    else:
        form = UserForm()
    return render(request, 'fetch/user_form.html', {'form': form})

def register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
