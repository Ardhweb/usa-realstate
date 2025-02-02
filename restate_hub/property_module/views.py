from django.shortcuts import render
from core.models import City,State,Country
from django.http import JsonResponse
import json
from property_module.forms import AddPropertiesInfoForm
# Create your views here.
def property_listing(request):
    states = State.objects.all() # Get all objects for now.
    context = {'states':states}
    return render(request,'property/listing.html',context)


from django.shortcuts import render, redirect

def add_property(request):
    if request.method == 'POST':
        form = AddPropertiesInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)  # Debugging: Print form validation errors
    else:
        form = AddPropertiesInfoForm()

    return render(request, 'property/add_property.html', {'form': form})

