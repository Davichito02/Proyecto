from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Create your serializers here.
class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)