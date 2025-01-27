from django.shortcuts import render,redirect
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
            username=cd['username'],
            password=cd['password']
            user = authenticate(request,
                                        username=cd['username'],
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
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def new_user_register(request):
    protocol = request.scheme  # 'http' or 'https'
    domain = request.get_host()  # e.g., 'example.com:8000'
    full_url = f"{protocol}://{domain}"
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid ():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user.is_active = False
            #new_user.is_email_verified = False
            six_digit=generate_secure_otp()
            sfa = SingleFactorEmailOTP.objects.create(user=new_user,six_otp=six_digit,attempts=1)
            url = reverse('accounts:email-code-verification', kwargs={'usr_id':new_user.id,'u_code':sfa.u_code})
            retreat_url = f'{full_url}{url}'
            send_email_sfa(subject='Email Verification', recipient_email=new_user.email,otp=six_digit,url=retreat_url)
            #user = authenticate(request, username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            # if user is not None:
            #     login(request, user)
            #     return redirect('membership_module:member_profile')
            # elif user.is_email_verified==False:
            #     return redirect('home')
            url = reverse('accounts:email-code-verification', kwargs={'usr_id':new_user.id,'u_code':sfa.u_code})
            return redirect(url)
            

    else:
        user_form = SignupForm()
    return render(request,'accounts/register.html',{'user_form': user_form})


def send_email_kode(request):

    return "s"

def email_kode_verifiy(request,usr_id,u_code):
    previous_url = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        forms = OTPVerificationForm(request.POST)
        submitted_otp = forms['otp']
        print(submitted_otp)
        code_sfa =SingleFactorEmailOTP(u_code=u_code,user_id=usr_id)
        if code_sfa.six_otp == submitted_otp:
            code_sfa.user.is_active==True
            return redirect("accounts:login")
        else:
            return HttpResponse("invalid email and otp")
    else:
        forms = OTPVerificationForm()
        context = {"forms":forms}
    return render(request,'utils/email_otp_verification.html',context)