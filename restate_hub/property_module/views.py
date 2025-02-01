from django.shortcuts import render
from core.models import City,State,Country
from django.http import JsonResponse
import json
# Create your views here.
def property_listing(request):
    states = State.objects.all() # Get all objects for now.
    context = {'states':states}
    return render(request,'property/listing.html',context)