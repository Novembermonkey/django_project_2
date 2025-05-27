from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from users.forms import LoginForm, RegisterModelForm
from django.contrib import messages

from users.models import CustomUser


# Create your views here.

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user:
                login(request, user)
                return redirect('shop:index')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Username or Password is incorrect"
                )

    return render(request, 'users/login.html', {'form': form})

def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('shop:index')

def register_page(request):
    form = RegisterModelForm()
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = False
            user.is_superuser = False
            user.save()
            login(request, user)
            return redirect('shop:index')


    return render(request, 'users/register.html', {"form": form})
