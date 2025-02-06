from django.shortcuts import render,redirect,get_object_or_404
from core.models import City,State,Country
from property_module.models import PropertiesInfo
from django.http import JsonResponse,Http404
import json
from property_module.forms import AddPropertiesInfoForm, ContactPartiesForm
from django.contrib.auth.decorators import login_required
from message_track.models import MessageTrack
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from property_module.utils import send_email_inquiry
# Create your views here.
def property_listing(request):
    states = State.objects.all() # Get all objects for now.
    context = {'states':states,}
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





@login_required()
def property_detail(request, property_id):
    property_obj = get_object_or_404(PropertiesInfo, property_id=property_id)
    try:
        messagetrack_obj = MessageTrack.objects.get(buyer=request.user.buyers, message_type='inquiry')
    except (MessageTrack.DoesNotExist, Exception) as e:
        messagetrack_obj = None  # No message track found, set to None
    if request.method == 'POST':
        form = ContactPartiesForm(request.POST)
        if form.is_valid():
            # Form submission logic here (if needed)
            seller = property_obj.seller  # Assuming `seller` exists on `PropertiesInfo`
            print(f"Seller email: {seller.email}")  # Debugging (remove later if not needed)
            subject=f'Request for Property: {property_obj.listing_id}'
            message=f'A buyer has interested in your property:{property_obj.listing_id} which if located at   {property_obj.street_name} , {property_obj.city}, zipcode: {property_obj.zipcode} according your property information.Please respond through'
            custom_msg=None
            sent_count = send_email_inquiry(subject, message, seller.email, custom_msg)
            if sent_count:
                message = MessageTrack.objects.create(
                buyer=request.user.buyers if request.user.is_authenticated else None, 
                seller=seller,
                message_out=message,
                message_type='inquiry')
                print("InquiryEmail sent successfully to  property owner!")
            else:
                print("Failed to send email.")

            url = reverse('property_module:property-details', args=[property_id])
            return redirect("home")
    else:
        form = ContactPartiesForm()
    return render(request, 'property/property_detail.html', {'property': property_obj, 'form': form,'messagetrack_obj':messagetrack_obj})