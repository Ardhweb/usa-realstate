from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/home.html')


def sign_up(request):
    return render(request, 'home/signup.html')

def login_page(request):
    return render(request, 'home/login.html')

def member_page(request):
    return render(request, 'home/member_profile.html')

def property_page(request):
    return render(request, 'home/property_listing.html')

def property_detail(request):
    return render(request, 'home/property_details.html')