from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated  # Allow any kind of authentication
from rest_framework.response import Response
from transactions_module.helcim import create_subscription,checkout_session
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.decorators import login_required
from django.http import Http404  
from transactions_module.models import HelcimInfo
from membership_module.models import SubscriptionPlans

@api_view(["GET"])  # Allows only GET requests
@permission_classes([AllowAny])  # Allows all users (authenticated & non-authenticated)
def checkout_view(request):
    if request.user.is_authenticated:  # Check if user is logged in
        checkoutCode = checkout_session(usr_id=request.user.id)  # Run the function
        
        return Response({"data": checkoutCode})  # Return the result
    else:
       raise Http404




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscription_api(request):
    # Ensure user is authenticated (already handled by the decorator)
    
    # Fetch the subscription plan for the user's member type
    plan = get_object_or_404(SubscriptionPlans, member_type=request.user.member_type)
    
    # Fetch Helcim info
    hInfo = get_object_or_404(HelcimInfo, user=request.user)
    
    # Create subscription
    subscribe = create_subscription(
        paymentPlanId=plan.paymentPlan,
        dateActive=hInfo.signup_date,
        usr_id=request.user.id
    )
    
    # Process subscription response
    if subscribe.get("status_code") in [200, 201] and "data" in subscribe:
        subscribe_data = subscribe["data"]
        
        # Update HelcimInfo
        hInfo.is_subscribed = True
        hInfo.subscriptionId = subscribe_data.get("id", "")
        hInfo.save()
        
        return Response({
            "message": "Subscription successful",
            "subscription_id": hInfo.subscriptionId
        }, status=201)
    
    return Response({
        "error": "Subscription failed",
        "details": subscribe
    }, status=400)

#update the helcimInfo table data is_susbcribed