from django.shortcuts import render
from apiroot.core.serializers import  CoreCountrySerializer , CoreCitySerializer, CoreStateSerializer
from core.models import Country , City , State
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




class CoreCity(APIView):
    ""
    @swagger_auto_schema(
        operation_description="This endpoint returns a list of all authors objects from records that we have.",
        responses={200: "Return all authors list via GET Method."}
    )
    def get(self, request, format=None):
        get_state = request.query_params.get('state', None)  # Get city from query params
        cities = City.objects.all()

        if get_state:
            cities = cities.filter(state__id=get_state)  # Case-insensitive filter

        serializer = CoreCitySerializer(cities, many=True)
        return Response(serializer.data)
        #api-root/core/states/?country=1
