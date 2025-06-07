from rest_framework import serializers
from .models import *


class UserAddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddresses
        fields = ('id', 'user_id', 'address_line_1', 'address_line_2', 'land_mark', 'phone_number', 'alternate_phone', 'city', 'state', 'pincode')

class UserRetriveSerializer(serializers.ModelSerializer):
    userAddresses = UserAddressDetailsSerializer(source='useraddresses_set', many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'email', 'profile_photo', 'userAddresses')

class UserListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'email', 'profile_photo')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'email', 'password', 'confirm_password')
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'error':"The passwords do not match."}, code='password_mismatch')
        return data
    
    def create(self, validated_data):
        validated_data ['is_admin'] = False
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user