from django.shortcuts import render
from apiroot.parties.serializers import PropertiesInfoSerializer
from property_module.models import PropertiesInfo
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from transactions_module.models import HelcimInfo

class PropertyList(APIView):
    #authentication_classes = []  # No automatic authentication
    permission_classes = [AllowAny]  # Allow all users (authenticated or not)

    """
    List of filtered properties by city in decsending order.
    GET /Propertis list by  user's selected city/
    """
    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all propertiesinfo objects from records that we have.",
        responses={200: "Return all propertiesinfo list via GET Method."}
    )
    def get(self, request, format=None):
        print(request.user.username)
        get_city = request.query_params.get('city', None)  # Get city from query params
        get_pagesize = request.query_params.get('perpage',10)

        # Validate before conversion
        if get_pagesize.isdigit():  
            get_pagesize = int(get_pagesize)
        else:
            get_pagesize = 10  # Default fallback
        
        print(get_pagesize)
        properties = PropertiesInfo.objects.none()

        if get_city:
            properties = PropertiesInfo.objects.filter(city__iexact=get_city).order_by('created_at')  # Case-insensitive filter
        # Limit to max 5 properties if user is not authenticated
        if not request.user.is_authenticated or request.user.user_helcim_account.is_subscribed == False:
            
            properties = properties[:5]
        else:
            properties = properties
        # Implement pagination
        paginator = PageNumberPagination()
        paginator.page_size = get_pagesize # Set default page size
        print()
        paginated_queryset = paginator.paginate_queryset(properties, request)

        serializer = PropertiesInfoSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
  
    #How to consume this :GET /api/properties/?city=New York


   