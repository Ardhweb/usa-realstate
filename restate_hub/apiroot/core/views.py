from django.shortcuts import render
from apiroot.core.serializers import  CoreCountrySerializer , CoreCitySerializer, CoreStateSerializer,CoreCountySerializer
from core.models import Country , City , State,County
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

class CoreCountry(APIView):
    ""
    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all authors objects from records that we have.",
        responses={200: "Return all authors list via GET Method."}
    )
    def get(self, request, format=None):
        countries = Country.objects.all()
        serializer = CoreCountrySerializer(countries, many=True)
        return Response(serializer.data)
        #api-root/core/countries

class CoreState(APIView):
    ""
    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all authors objects from records that we have.",
        responses={200: "Return all authors list via GET Method."}
    )
    def get(self, request, format=None):
        get_country = request.query_params.get('country', None)  # Get city from query params
        states = State.objects.all()

        if get_country:
            states = states.filter(country__id=get_country)  # Case-insensitive filter

        serializer =CoreStateSerializer(states, many=True)
        return Response(serializer.data)
        #api-root/core/states/?country=1


class CoreCounty(APIView):
    ""
    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all the counties or any specific county objects from records that we have to  respactive there state.",
        responses={200: "Return counties via GET Method."}
    )
    def get(self, request, format=None):
        get_state = request.query_params.get('state', None)  # Get state from query params
        counties = County.objects.all()
        if get_state:
            counties = counties.filter(state__id=get_state)  # Case-insensitive filter

        serializer = CoreCountySerializer(counties, many=True)
        return Response(serializer.data)
        #api-root/core/states/?county=1


class CoreCity(APIView):
    ""
    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all authors objects from records that we have.",
        responses={200: "Return all authors list via GET Method."}
    )
    def get(self, request, format=None):
        get_state = request.query_params.get('state', None)  # Get city from query params
        get_county = request.query_params.get('county', None)
        
        cities = City.objects.all()
       
        if get_state:
            cities = cities.filter(state__id=get_state)  # Case-insensitive filter
        
        if get_county:
            cities = cities.filter(county__id=get_county) 

        serializer = CoreCitySerializer(cities, many=True)
        return Response(serializer.data)
        #api-root/core/states/?country=1




