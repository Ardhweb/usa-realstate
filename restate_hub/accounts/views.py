from django.shortcuts import render,redirect,get_object_or_404
from django.http import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout 
from .forms import LoginForm, SignupForm ,OTPVerificationForm 
from django.contrib import auth, messages
from accounts.models import SingleFactorEmailOTP
import secrets
from accounts.utils import send_email_sfa
from django.urls import reverse
from django.utils.timezone import now
from django.contrib import messages
from buyer_module.models import Buyers
from seller_module.models import Sellers
from agent_module.models import Agents
from django.db import transaction
from transactions_module.helcim import create_customer_helcim
from transactions_module.models import HelcimInfo
# views.py



def generate_secure_otp(length=6):
    return ''.join(secrets.choice('0123456789') for _ in range(length))


def user_logout(request):
    logout(request)
    return redirect("home")
    
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                        username=cd['username_or_email'],
                                        password=cd['password'])
            if user is not None:
                #verificatikn logic checking user
                if user.is_active and user.is_email_verified==True: #and user.is_phone_verified==True:
                    login(request, user)
                    return redirect("property_module:property-listing")
                elif user.is_active and user.is_email_verified==False:
                    login(request, user)
                    #return to property listing
                    return redirect("membership_module:member_profile")
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, "Invalid login!")
            return redirect("membership_module:member_profile")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def new_user_register(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            with transaction.atomic():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                member = new_user.member_type
                if member == 'buyer':
                    Buyers.objects.create(user=new_user)
                elif member == 'seller':
                    Sellers.objects.create(user=new_user)
                elif member == 'agent':
                    Agents.objects.create(user=new_user)
                else:
                    messages.error(request, "Invalid member type")
                return redirect('accounts:login')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, error)  # Use Django's system error messages directly
    else:
        user_form = SignupForm()
    
    return render(request, 'accounts/register.html', {'user_form': user_form})



