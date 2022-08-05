from rest_framework import serializers
from django.contrib.auth import authenticate

from retailers.models import Retailer
from users.models import User
from users.serializers import RegistrationSerializer, LoginSerializer


class RetailerRegistrationSerializer(RegistrationSerializer):
    street = serializers.CharField(allow_null=False, allow_blank=False)
    city = serializers.CharField(allow_null=False, allow_blank=False)
    state = serializers.CharField(allow_null=False, allow_blank=False)

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['is_staff'] = True
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        # create retailer profile
        retailer = Retailer.objects.create(user=user)
        retailer.save()
        return retailer


class RetailerLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        users = User.objects.all()
        user = users.filter(email=email)

        if user:
            authenticated_user = authenticate(username=email, password=password)
            print(authenticated_user)
            if not authenticated_user or not authenticated_user.is_staff:
                raise serializers.ValidationError('Invalid login details provided')
            attrs['user'] = authenticated_user
            return attrs
        else:
            raise serializers.ValidationError('Invalid email or password')