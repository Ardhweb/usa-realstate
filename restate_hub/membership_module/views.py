from django.shortcuts import render,redirect
from seller_module.models import Sellers
from property_module.models import PropertiesInfo
from accounts.models import User
# Create your views here.
from django.http import JsonResponse,Http404
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from membership_module.models import MembershipFee, MemberAddress,DefaultFeeStructure
from buyer_module.models import Buyers
from agent_module.models import Agents
from django.db.models import F
from django.forms.models import model_to_dict

def generate__address(data):
    defaults = {}
    if "buyer_id" in data: defaults["buyer_id"] = data["buyer_id"]
    if "seller_id" in data: defaults["seller_id"] = data["seller_id"]
    if "agent_id" in data: defaults["agent_id"] = data["agent_id"]
    
    member_address, created = MemberAddress.objects.update_or_create(
        street_no=data.get("street_no"),
        street_name=data.get("street_name"),
        city=data.get("city"),
        state=data.get("state"),
        zip_code=data.get("zip_code"),
        member_type=data.get("member_type"),
        defaults=defaults
    )

    return member_address.id


@login_required
def member_profile(request):  
    if request.method == 'POST':
        # Retrieve form data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        street_number = request.POST.get('street_number')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        has_agent = request.POST.get('has_agent')
        agent_first_name = request.POST.get('agent_first_name') if has_agent == 'yes' else None
        agent_last_name = request.POST.get('agent_last_name') if has_agent == 'yes' else None
        agent_phone = request.POST.get('agent_phone') if has_agent == 'yes' else None
        agent_email = request.POST.get('agent_email') if has_agent == 'yes' else None
        business_name = request.POST.get('business_name')
        one_time_fee = request.POST.get('one_time_fee')
        monthly_fee = request.POST.get('monthly_fee')
        total = request.POST.get('total')
        send_question = request.POST.get('send_question')
        # Get the current logged-in user
        user = request.user
        address_id = None
        address = {
            "street_no":street_number,
            "street_name":street_address,
            "city":city,
            "state":state,
            "zip_code":zip_code,
            "member_type":user.member_type,
           
        }
       
        match request.user.member_type:
            case 'buyer':
                buyer, created = Buyers.objects.get_or_create(user=request.user)
                buyer.first_name = first_name
                buyer.last_name = last_name
                buyer.phone_num = phone
                buyer.email = email
                buyer.business_name = business_name
                buyer.save()
                print(buyer.id)
                address['buyer_id'] = buyer.id
                address_id = generate__address(address)
            case 'seller':
                seller, created = Sellers.objects.get_or_create(user=user)
                seller.first_name = first_name
                seller.last_name = last_name
                seller.phone_num = phone
                seller.email = email
                seller.business_name = business_name
                seller.save()
                address['seller_id'] = seller.id
                address_id = generate__address(address)
            case 'agent':
                agent, created = Agents.objects.get_or_create(user=user)
                agent.first_name = first_name
                agent.last_name = last_name
                agent.phone_num = phone
                agent.email = email
                agent.business_name = business_name
                agent.save()
                address_id = generate__address(address)
        # Create the MembershipFee record
        MembershipFee.objects.update_or_create(
            acct_setup_fee=one_time_fee,
            membership_fee=monthly_fee,
            defaults = {"maddress_id":address_id})
           
        

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
        return redirect('membership_module:profile_success')
    else:
        profile_data = None
        unified = None
    
        # Handle the different user member types
        match request.user.member_type:
            case 'buyer':
                profile_data = Buyers.objects.get(user=request.user)
                agent_data = {}
              
                
                try:
                    agent = profile_data.agent
                    # Fetch agent and related data
                    agents = Agents.objects.get(id=agent.id) if agent else None
                    agent_data = {f"agents_{k}": v for k, v in model_to_dict(agents).items()} if agents else {}
    
                    # Fetch address and membership fee for the buyer
                    address = MemberAddress.objects.get(buyer_id=profile_data.id)
                    fee = MembershipFee.objects.get(maddress_id=address.id)
                    address_data = {f"{k}": v for k, v in model_to_dict(address).items()}
                    fee_data = {f"{k}": v for k, v in model_to_dict(fee).items()}
                except (MemberAddress.DoesNotExist, MembershipFee.DoesNotExist):
                    address_data, fee_data, agent_data = {}, {}, {}
    
                # Start with the profile data and merge
                unified = model_to_dict(profile_data)
                unified.update(address_data)
                unified.update(fee_data)
                unified.update(agent_data)
              
    
            case 'seller':
                profile_data = Sellers.objects.get(user=request.user)
                
                agent_data = {}
                try:
                    agent = profile_data.agent
                    # Fetch agent and related data
                    agents = Agents.objects.get(id=agent.id)if agent else None
                    agent_data = {f"agents_{k}": v for k, v in model_to_dict(agents).items()} if agents else {}
                  
    
                    # Fetch address and membership fee for the seller
                    address = MemberAddress.objects.get(seller_id=profile_data.id)
                    fee = MembershipFee.objects.get(maddress_id=address.id)
                    address_data = {f"{k}": v for k, v in model_to_dict(address).items()}
                    fee_data = {f"{k}": v for k, v in model_to_dict(fee).items()}
                except (MemberAddress.DoesNotExist, MembershipFee.DoesNotExist):
                    address_data, fee_data, agent_data = {}, {}, {}
    
                # Start with the profile data and merge
                unified = model_to_dict(profile_data)
                unified.update(address_data)
                unified.update(fee_data)
                unified.update(agent_data)
            case 'agent':
                profile_data = Agents.objects.get(user=request.user)
                agent_data = {}
                try:
                    # Fetch address and membership fee for the seller
                    address = MemberAddress.objects.get(seller_id=profile_data.id)
                    fee = MembershipFee.objects.get(maddress_id=address.id)
                    address_data = {f"{k}": v for k, v in model_to_dict(address).items()}
                    fee_data = {f"{k}": v for k, v in model_to_dict(fee).items()}
                except (MemberAddress.DoesNotExist, MembershipFee.DoesNotExist):
                    address_data, fee_data, agent_data = {}, {}, {}
    
                # Start with the profile data and merge
                unified = model_to_dict(profile_data)
                unified.update(address_data)
                unified.update(fee_data)
                unified.update(agent_data)
    
            case _:
                profile_data = None
                unified = None
        #print(unified)
    return render(request, 'members/profile.html', {'profile_data': profile_data or {}, "data": unified or {}})



def profile_success(request):
    return render(request, 'members/profile_success.html')




