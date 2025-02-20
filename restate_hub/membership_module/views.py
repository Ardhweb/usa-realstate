from django.shortcuts import render,redirect
from seller_module.models import Sellers
from property_module.models import PropertiesInfo
from accounts.models import User
# Create your views here.
from django.http import JsonResponse,Http404
import json
from property_module.forms import AddPropertiesInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from membership_module.models import MembershipFee, MemberAddress
from buyer_module.models import Buyers
from agent_module.models import Agents
from django.db.models import F
from django.forms.models import model_to_dict

def generate__address(data):
    member_address = MemberAddress.objects.create(
        street_no=data.get("street_no"),
        street_name=data.get("street_name"),
        city=data.get("city"),
        state=data.get("state"),
        zip_code=data.get("zip_code"),
        member_type=data.get("member_type"),
        buyer_id = data.get('buyer_id', None),
        seller_id = data.get('seller_id', None),
        agent_id = data.get('agent_id', None),
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
        print(address_id)

        # Create the MembershipFee record
        MembershipFee.objects.create(
            acct_setup_fee=one_time_fee,
            membership_fee=monthly_fee,
            maddress_id=address_id
        )

        # 🌟 **Handle Agent Assignment**
        if has_agent == 'yes':
            agent, created = Agents.objects.get_or_create(
                first_name=agent_first_name,
                last_name=agent_last_name,
                phone_num=agent_phone,
                email=agent_email
            )

            # Link the agent to the buyer or seller
            if user.member_type == 'buyer':
                buyer.agent = agent
                buyer.save()
            elif user.member_type == 'seller':
                seller.agent = agent
                seller.save()

        # Handle the message to admin (if required)
        if send_question:
            # Code to send message to the admin (e.g., via email or saving it to a database)
            pass

        # Redirect to the profile success page
        return redirect('membership_module:profile_success')

    else:
       
        match request.user.member_type:
            case 'buyer':
                profile_data = Buyers.objects.get(user=request.user)
                address = MemberAddress.objects.get(buyer_id=profile_data.id)
                fee = MembershipFee.objects.get(maddress_id=address.id)
                address_data = {f"{k}": v for k, v in model_to_dict(address).items()}
                fee_data = {f"{k}": v for k, v in model_to_dict(fee).items()}
                unified = {**model_to_dict(profile_data), **address_data,**fee_data}
                print(unified)
            case 'seller':
                profile_data = Sellers.objects.get(user=request.user)
                address = MemberAddress.objects.get(seller_id=profile_data.id)
                fee = MembershipFee.objects.get(maddress_id=address.id)
                address_data = {f"{k}": v for k, v in model_to_dict(address).items()}
                fee_data = {f"{k}": v for k, v in model_to_dict(fee).items()}
                unified = {**model_to_dict(profile_data), **address_data,**fee_data}
                print(unified)
            case _:
                profile_data = None
    return render(request, 'members/profile.html', {'profile_data':profile_data or {}, "data":unified or {}})


def profile_success(request):
    return render(request, 'members/profile_success.html')


@login_required() 
def member_dashboard(request):
    if request.user.is_authenticated:
        seller = Sellers.objects.get(user=request.user)
        total_property = PropertiesInfo.objects.filter(seller=seller).count()
        sold_property = PropertiesInfo.objects.filter(listing_status='sold').count()
        return render(request, "members/dashboard.html", {'active_page':'dashboard', "total_property":total_property,'sold_property': sold_property})
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


