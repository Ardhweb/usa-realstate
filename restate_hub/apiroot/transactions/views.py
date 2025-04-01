from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated  # Allow any kind of authentication
from rest_framework.response import Response
from transactions_module.helcim import create_subscription

@api_view(["POST"])
@permission_classes([IsAuthenticated])   # Allow any kind of authentication method
def subscription_api(request):
    # In Session Authentication, request.user will automatically be populated based on the session.
    # We do not need to pass any credentials in the request.
    if request.user.is_authenticated:
        # Process the request for authenticated users
        susbcribe = create_subscription(paymentPlanId=11991,dateActive="2025-04-01",usr_id=request.user.id)
        response_data = {"user_id": request.user.id}  # Example response data
        return Response(response_data)
    else:
        return Response({"error": "Authentication required"}, status=403)
