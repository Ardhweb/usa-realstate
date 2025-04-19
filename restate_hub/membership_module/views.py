from django.shortcuts import render,redirect
from seller_module.models import Sellers
from property_module.models import PropertiesInfo
from accounts.models import User
# Create your views here.
from django.http import JsonResponse,Http404
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from membership_module.models import MembershipFee, MemberAddress
from buyer_module.models import Buyers
from agent_module.models import Agents
from django.db.models import F
from django.forms.models import model_to_dict
from core.models import State, City

'''
def generate__address(data):
    # defaults = {}
    # if "buyer_id" in data: defaults["buyer_id"] = data["buyer_id"]
    # if "seller_id" in data: defaults["seller_id"] = data["seller_id"]
    # if "agent_id" in data: defaults["agent_id"] = data["agent_id"]
    member_address, created = MemberAddress.objects.update_or_create(
        street_no=data.get("street_no"),
        street_name=data.get("street_name"),
        city_id=data.get("city_id"),
        state_id=data.get("state_id"),
        zip_code=data.get("zip_code"),
        member_type=data.get("member_type"),
        user_id=data.get('user_id'),
        # defaults=defaults
    ) 

    return member_address.id
'''
def generate__address(data):
    user_id = data.get("user_id")

    try:
        member_address = MemberAddress.objects.get(user_id=user_id)
        # Update the existing address
        member_address.street_no = data.get("street_no")
        member_address.street_name = data.get("street_name")
        member_address.city_id = data.get("city_id")
        member_address.state_id = data.get("state_id")
        member_address.zip_code = data.get("zip_code")
        member_address.member_type = data.get("member_type")
        member_address.save()
    except MemberAddress.DoesNotExist:
        # Create a new address if one doesn't exist
        member_address = MemberAddress.objects.create(
            user_id=user_id,
            street_no=data.get("street_no"),
            street_name=data.get("street_name"),
            city_id=data.get("city_id"),
            state_id=data.get("state_id"),
            zip_code=data.get("zip_code"),
            member_type=data.get("member_type")
        )

    return member_address.id



def validate_fields(request, first_name=None, last_name=None, phone=None,
                    street_number=None, street_address=None, 
                    zip_code=None, business_name=None):
    errors_exist = False  # Flag to check if errors were added

    # Required fields validation
    required_fields = {
        "First name": first_name,
        "Last name": last_name,
        "Phone": phone,
        "Street number": street_number,
        "Street address": street_address,
        "Zip code": zip_code,
        "Business name": business_name,
    }

    for field_name, value in required_fields.items():
        if value is None or not str(value).strip():  # Check if value is None or empty
            messages.error(request, f"{field_name} is required.")
            errors_exist = True

    # Numeric fields validation
    numeric_fields = {"Zip code": zip_code}
    
    for field_name, value in numeric_fields.items():
        if value and not str(value).isdigit():
            messages.error(request, f"{field_name} must be a valid number.")
            errors_exist = True

    # Max length validation
    max_length_fields = {
        "First name": 50,
        "Last name": 50,
        "Phone": 15,
        "Street number": 10,
        "Street address": 100,
        "Zip code": 10,
        "Business name":50
    }

    for field_name, max_length in max_length_fields.items():
        value = required_fields.get(field_name)
        if value and len(value) > max_length:
            messages.error(request, f"{field_name} must not exceed {max_length} characters.")
            errors_exist = True

    # Phone number length validation
    '''if phone and (len(phone) < 10 or len(phone) > 15):
        messages.error(request, "Phone number must be between 10 and 15 digits.")
        errors_exist = True'''

    return errors_exist if errors_exist else None  # Return None if no errors exist


@login_required
def member_profile(request):  
    if request.method == 'POST':
        # Retrieve form data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        street_number = request.POST.get('street_number')
        street_address = request.POST.get('street_address')
        city = int(request.POST.get('city'))
        state = int(request.POST.get('state'))
        zip_code = request.POST.get('zip_code')
        has_agent = request.POST.get('has_agent')
        agent_first_name = request.POST.get('agent_first_name') if has_agent == 'yes' else None
        agent_last_name = request.POST.get('agent_last_name') if has_agent == 'yes' else None
        agent_phone = request.POST.get('agent_phone') if has_agent == 'yes' else None
        agent_email = request.POST.get('agent_email') if has_agent == 'yes' else None
        business_name = request.POST.get('business_name')
        send_question = request.POST.get('send_question')
        #validation:
        # validation_errors = validate_fields(request, first_name, last_name, phone, 
        #                         street_number, street_address,zip_code, business_name)
        # if validation_errors:  # If there are errors, redirect back to the profile page
        #     return redirect('membership_module:member_profile')
        
        # Proceed with saving data since validation passed
        # Get the current logged-in user
        user = request.user
        #update user fields
        user.first_name = first_name
        user.last_name = last_name
        user.contact_no  = phone # getting error 
        user.save()
        
        address_id = None
        address = {
            "street_no":street_number,
            "street_name":street_address,
            "city_id":city,
            "state_id":state,
            "zip_code":zip_code,
            "member_type":user.member_type,
            "user_id":request.user.id,
           
        }
        match request.user.member_type:
            case 'buyer':
                buyer, created = Buyers.objects.get_or_create(user=request.user)
                buyer.business_name = business_name
                buyer.save()
                print(buyer.id)
                #address['buyer_id'] = buyer.id
                address_id = generate__address(address)
            case 'seller':
                seller, created = Sellers.objects.get_or_create(user=user)
                seller.business_name = business_name
                seller.save()
                #address['seller_id'] = seller.id
                address_id = generate__address(address)
            case 'agent':
                agent, created = Agents.objects.get_or_create(user=user)
                agent.business_name = business_name
                agent.save()
                address_id = generate__address(address)
      
        # 🌟 **Handle Agent Assignment**
        if has_agent == 'yes':
            # agent = Agents.objects.get(
            #     email=agent_email
            # )
            try:
                agent = Agents.objects.get(email=agent_email)
            except Agents.DoesNotExist:
                agent = None
            # Link the agent to the buyer or seller
            if user.member_type == 'buyer':
                buyer.agent = agent
                buyer.save()
            elif user.member_type == 'seller':
                seller.agent = agent
                seller.save()
        else:
             # Link the agent to the buyer or seller
            if user.member_type == 'buyer':
                buyer.agent = None
                buyer.save()
            elif user.member_type == 'seller':
                seller.agent = None
                seller.save()
        # Handle the message to admin (if required)
        if send_question:
            # Code to send message to the admin (e.g., via email or saving it to a database)
            pass

        # Redirect to the profile success page
        return redirect('membership_module:member_profile')
    else:
        cities = City.objects.all()
        states = State.objects.all()
        context = {
            'cities':cities,
            'states':states,
        }
        return render(request, 'members/profile.html',context)





