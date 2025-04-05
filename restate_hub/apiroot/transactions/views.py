from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated  # Allow any kind of authentication
from rest_framework.response import Response
from transactions_module.helcim import create_subscription,checkout_session
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.decorators import login_required
from django.http import Http404  
from transactions_module.models import HelcimInfo
from membership_module.models import SubscriptionPlans
import uuid

def generate_alphanumeric_uuid_25():
    full_uuid = str(uuid.uuid4()).replace("-", "")  # Remove hyphens
    return full_uuid[:25]  # Ensure exactly 25 alphanumeric characters

# Generate and print both UUIDs
uuid_25 = generate_alphanumeric_uuid_25()


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
from rest_framework.decorators import api_view, permission_classes,  authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
import requests
import uuid
import json
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.conf import settings


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def subscription_api(request):
    if not request.user.is_authenticated:
        return Response("User is not authenticated", status=403, content_type="text/plain")

    try:
        # Fetch required data
        plan = get_object_or_404(SubscriptionPlans, member_type=request.user.member_type)
        hInfo = get_object_or_404(HelcimInfo, user=request.user)
        date_activated_str = hInfo.signup_date.isoformat()
        print(date_activated_str)

        # Prepare API request
        url = "https://api.helcim.com/v2/subscriptions"
        payload = {
            "subscriptions": [{
                "paymentMethod": "card",
                "paymentPlanId": plan.paymentPlan,
                "customerCode": f"CST{request.user.id}",
                "useCustomSetupAmount": True,
                "setupAmount": 0.2,
                "recurringAmount": 01.00,
                "withFreeTrialPeriod": False,
                "dateActivated":f"{date_activated_str}",
            }]
        }
        headers = {
            "accept": "application/json",
            "api-token": settings.HELCIM_API_TOKEN,
            "idempotency-key": uuid_25,
            "content-type": "application/json"
        }

        # Send request
        response = requests.post(url, json=payload, headers=headers)
        raw_response_text = response.text  # Get exact response text

        # Print and return exact response
        print(f"Helcim Response:{raw_response_text}")
        # Log request and response
        # Attempt to parse response manually
        try:
            response_data = json.loads(raw_response_text)  # Convert text to dictionary
            subscription_id = response_data.get("data", [{}])[0].get("id", None)  # Extract ID safely
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response from Helcim.")
            return Response({"error": "Invalid response format from Helcim", "details": raw_response_text}, status=502)
        match response.status_code:
            case 201:
                print("✅ Success! Subscription created successfully.")
                hInfo.is_subscribed = True
                hInfo.subscriptionId = subscription_id
                hInfo.subscription_status = 'active'
                hInfo.save()
            case 400:
                print("⚠️ Bad Request! There may be missing or incorrect parameters.")
            case 401:
                print("⛔ Unauthorized! Check your API credentials.")
            case 403:
                print("🚫 Forbidden! You do not have permission to access this resource.")
            case _:
                print(f"❓ Unexpected response: {response.status_code} - {response.text}")
        return Response(raw_response_text,status=response.status_code, content_type="application/json")

    except Exception as e:
        print(str(e))
        return Response(str(e), status=500, content_type="text/plain")