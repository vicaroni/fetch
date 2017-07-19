from django.shortcuts import render, redirect, get_object_or_404
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserForm, RegisterForm
from .models import UserRepository, DeployKey

# Create your views here.
@login_required
def key_list(request):
    return render(request, 'fetch/key_list.html', {'user': request.user})

@login_required
def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            token = form.save(commit=False)
            token.user = request.user
            token.save()
            return redirect('key_list')
    else:
        form = UserForm()
    return render(request, 'fetch/user_form.html', {'form': form})

@login_required
def key_download(request):
    user = request.user
    call_command('key_download', user.username, user.tokens.first().token)
    return redirect('key_list')

def register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
