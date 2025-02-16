from django.shortcuts import render
from seller_module.models import Sellers
from property_module.models import PropertiesInfo
from accounts.models import User
# Create your views here.
from django.http import JsonResponse,Http404
import json
from property_module.forms import AddPropertiesInfoForm
from django.contrib.auth.decorators import login_required

def memebers_profile(request):
    return render(request,'members/profile.html')

@login_required() 
def member_dashboard(request):
    if request.user.is_authenticated:
        seller = Sellers.objects.get(user=request.user)
        total_property = PropertiesInfo.objects.filter(seller=seller).count()
        return render(request, "members/dashboard.html", {'active_page':'dashboard', "total_property":total_property})
    else:
        return redirect('home')

@login_required() 
def my_property(request):
    if request.user.is_authenticated:
        seller = Sellers.objects.get(user_id=request.user.id)
        if request.user.member_type == 'seller':
            properties  = PropertiesInfo.objects.filter(seller=seller)
            return render(request, "members/my_property.html", {'properties':properties,'active_page':'my-property'})
        else:
            return redirect('accounts:login')
    else:
        return redirect('accounts:login')


@login_required()  # Ensures user is logged in
def add_property(request):
    if request.user.is_authenticated and request.user.member_type == 'seller' or request.user.member_type == 'agent':
        if request.method == 'POST':
            form = AddPropertiesInfoForm(request.POST,request.FILES)
            seller =  Sellers.objects.get(user=request.user)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.seller = seller
                instance.save()
                return redirect('membership_module:my_property')
            else:
                print(form.errors)  # Debugging: Print form validation errors
        else:
            form = AddPropertiesInfoForm()
        return render(request, 'members/add_property.html', {'form': form,'active_page':'add-property'})
    else:
        raise Http404('Page not found')

@login_required()  
def view_message(request):
    return render(request, "members/message.html", {'active_page':'view-message'})


