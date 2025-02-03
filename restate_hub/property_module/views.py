from django.shortcuts import render,redirect
from core.models import City,State,Country
from property_module.models import PropertiesInfo
from django.http import JsonResponse,Http404
import json
from property_module.forms import AddPropertiesInfoForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def property_listing(request):
    states = State.objects.all() # Get all objects for now.
    recent_properties = PropertiesInfo.objects.all()

    context = {'states':states,'recent_properties':recent_properties}
    return render(request,'property/listing.html',context)



@login_required()  # Ensures user is logged in
def add_property(request):
    if request.user.is_authenticated and request.user.member_type == 'seller' or request.user.member_type == 'agent':
        if request.method == 'POST':
            form = AddPropertiesInfoForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                #instance.seller = None
                instance.save()
                return redirect('home')
            else:
                print(form.errors)  # Debugging: Print form validation errors
        else:
            form = AddPropertiesInfoForm()
        return render(request, 'property/add_property.html', {'form': form})
    else:
        raise Http404('Page not found')

