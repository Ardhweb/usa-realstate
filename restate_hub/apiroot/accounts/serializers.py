from accounts.models import User
from rest_framework import serializers
from agent_module.models import Agents

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agents
        fields = '__all__'

