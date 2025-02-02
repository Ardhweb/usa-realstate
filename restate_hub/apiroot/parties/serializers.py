from property_module.models import  PropertiesInfo
from rest_framework import serializers

class PropertiesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertiesInfo
        fields = '__all__'