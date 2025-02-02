from django.shortcuts import render
from apiroot.parties.serializers import PropertiesInfoSerializer
from property_module.models import PropertiesInfo
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class PropertyList(APIView):
    """
    List of all authors.
    GET /authors/
    """
    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all authors objects from records that we have.",
        responses={200: "Return all authors list via GET Method."}
    )
    def get(self, request, format=None):
        properties = PropertiesInfo.objects.all()
        serializer = PropertiesInfoSerializer(properties, many=True)
        return Response(serializer.data)

   