from django.shortcuts import render

# Create your views here.

def memebers_profile(request):
    return render(request,'members/profile.html')