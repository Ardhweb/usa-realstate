from django.shortcuts import render,redirect
from django.http import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout 
from .forms import LoginForm, SignupForm                                     
from django.contrib import auth, messages

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                        username=cd['username'],
                                        password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    
        
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def new_user_register(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid ():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('home')
    else:
        user_form = SignupForm()
    return render(request,'accounts/register.html',{'user_form': user_form})
