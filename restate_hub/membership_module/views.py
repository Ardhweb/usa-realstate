from django.shortcuts import render, redirect
from django.contrib import messages
from membership_module.models import MembershipFee, MemberAddress
from buyer_module.models import Buyers
from seller_module.models import Sellers  # Import Sellers model
from agent_module.models import Agents
from accounts.models import User
from django.contrib.auth.decorators import login_required

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

        # Create or update the MemberAddress record
        member_address = MemberAddress.objects.create(
            street_no=street_number,
            street_name=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            member_type=user.member_type,
        )

        # 🌟 **Handle Buyer Logic**
        if user.member_type == 'Buyer':
            buyer, created = Buyers.objects.get_or_create(user=user)
            buyer.first_name = first_name
            buyer.last_name = last_name
            buyer.phone_num = phone
            buyer.email = email
            buyer.business_name = business_name
            buyer.save()

        # 🌟 **Handle Seller Logic**
        elif user.member_type == 'Seller':
            seller, created = Sellers.objects.get_or_create(user=user)
            seller.first_name = first_name
            seller.last_name = last_name
            seller.phone_num = phone
            seller.email = email
            seller.business_name = business_name
            seller.save()

        # Create the MembershipFee record
        MembershipFee.objects.create(
            acct_setup_fee=one_time_fee,
            membership_fee=monthly_fee,
            maddress=member_address
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
            if user.member_type == 'Buyer':
                buyer.agent = agent
                buyer.save()
            elif user.member_type == 'Seller':
                seller.agent = agent
                seller.save()

        # Handle the message to admin (if required)
        if send_question:
            # Code to send message to the admin (e.g., via email or saving it to a database)
            pass

        # Redirect to the profile success page
        return redirect('membership_module:profile_success')

    else:
        # GET request - render the member profile form
        return render(request, 'members/profile.html')

def profile_success(request):
    return render(request, 'members/profile_success.html')