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
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def new_user_register(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid ():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user = authenticate(request, username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
            return redirect('membership_module:member_profile')   
    else:
        user_form = SignupForm()
    return render(request,'accounts/register.html',{'user_form': user_form})


def resend_email_kode(request):

    return "s"

def email_kode_verifiy(request,usr_id,u_code):
    previous_url = request.META.get('HTTP_REFERER', '/')
    url = reverse('accounts:email-code-verification', kwargs={'usr_id':usr_id,'u_code':u_code})
    code_instance = get_object_or_404(SingleFactorEmailOTP, u_code=u_code)

    if code_instance.has_expired():
        messages.error(request, "This OTP has expired. Please request a new one only valid for 24hours.")
        return redirect('resend_otp')  # Or handle regeneration

    if not code_instance.is_expired:
        messages.error(request, "This OTP is no longer valid due to too many failed attempts.")
        # return redirect('resend_otp')
        return redirect(url)

    if request.method == 'POST':
        forms = OTPVerificationForm(request.POST)
        if forms.is_valid():
            submitted_otp = forms.cleaned_data['otp']
            if code_instance.six_otp == submitted_otp:
                code_instance.is_expired = False  # Mark OTP as used
                code_instance.save()
                code_instance.user.is_active==True
                messages.success(request, "OTP verified successfully!")
                return redirect('home')
            else:
                code_instance.increment_attempts()
                if not code_instance.is_expired:
                    messages.error(request, "Too many failed attempts. OTP is now blocked.")
                    # return redirect('resend_otp')
                    return redirect(url)
                else:
                    messages.error(request, f"Invalid OTP. {otp_instance.max_attempts -code_instance.attempts} attempts left.")
                    # return redirect("accounts:login")
                    return redirect(url)     
    else:
        forms = OTPVerificationForm()
        context = {"forms":forms}
    return render(request,'utils/email_otp_verification.html',context)