from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from apiroot.accounts.serializers import UserSerializer , AgentSerializer
from accounts.models import User
from agent_module.models import Agents
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AccountsUser(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all user objects.",
        responses={200: openapi.Response("Return all users list via GET Method.")}
    )
    def get(self, request, format=None):
        if request.user.is_superuser:
            users = User.objects.all().values()  # Get data as a dictionary
            return Response({"data": list(users)})  # Convert to list and return JSON response
        return Response({"data": []})  # Return empty data if not superuser
        #api-root/accounts/users


class AgentsAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all the agent objects.",
        responses={200: openapi.Response("Return all users list via GET Method.")}
    )
    
    def get(self, request, format=None):
        if request.user.is_authenticated:
            email = request.query_params.get("email")  # Get email from query params
            
            if not email:
                return Response({"error": "Email parameter is required."}, status=400)

            try:
                agent = User.objects.get(email=email)  # Fetch agent by email
                return Response({"email": agent.email})  # Only return the email
            except ObjectDoesNotExist:
                return Response({"error": "Agent not found."}, status=404)

        return Response({"error": "Unauthorized access."}, status=403)


