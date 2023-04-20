from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import Box

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data
    
class RefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data
    
class BoxSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='user.username')
    last_updated_by = serializers.ReadOnlyField(source='updated_by.username')
    last_updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Box
        fields = ('id', 'length', 'breadth', 'height', 'area', 'volume', 'created_by', 'last_updated', 'last_updated_by')
        read_only_fields = ('area', 'volume', 'created_by', 'last_updated', 'last_updated_by')