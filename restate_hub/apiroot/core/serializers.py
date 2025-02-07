from core.models import Country , City , State
from rest_framework import serializers

class  CoreCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class  CoreStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class  CoreCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'