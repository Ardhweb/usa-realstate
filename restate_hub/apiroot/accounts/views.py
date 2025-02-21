from django.shortcuts import render
from apiroot.accounts.serializers import UserSerializer 
from accounts.models import User
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

