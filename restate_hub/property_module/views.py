from django.shortcuts import render,redirect,get_object_or_404
from core.models import City,State,Country
from property_module.models import PropertiesInfo
from django.http import JsonResponse,Http404
import json
from property_module.forms import AddPropertiesInfoForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def property_listing(request):
    states = State.objects.all() # Get all objects for now.
    context = {'states':states,}
    return render(request,'property/listing.html',context)

def property_detail(request, property_id):
    property = get_object_or_404(PropertiesInfo, pk=property_id)
    return render(request, 'property/property_detail.html', {'property': property})

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



from django.http import JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404
from message_track.models import MessageTrack
from property_module.models import PropertiesInfo
from agent_module.models import Agents
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from property_module.forms import ContactPartiesForm

def property_detail(request, property_id):
    property = get_object_or_404(PropertiesInfo, property_id=property_id)
    if request.method == 'POST':
        forms = ContactPartiesForm(request.POST)
        seller = property.seller #For because for nowwe sending only seller
        print(f"{seller.email}")
        # message = MessageTrack.objects.create(
        #    message_type='buyer_to_seller_request',
        #    sender_id=request.user.id if request.user.is_authenticated else None,  # Assuming user is Buyer. You'll need user auth
        #    receiver_id=seller.id,
        #    message_content=f"Buyer requested info for property: {property.street_name}.",
        #  )
        #  # Send email to seller
        #  subject = f'Request for Property: {property.street_name}'
        #  message_body = f'A buyer has requested information about your property: {property.street_name}. Please respond through your email'

        #  send_mail(subject, message_body, settings.EMAIL_HOST_USER, [seller.email], fail_silently=False)
        #  message.status = 'sent'
        #  message.related_entity_id = seller.id
        #  message.save()
        url = reverse('property_module:property-details', args=[property_id])
        return redirect(url)
    else:
        return render(request, 'property/property_detail.html', {'property': property})

