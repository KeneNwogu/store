from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Wishlist


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        # create wishlist for user
        wishlist = Wishlist(user=user)
        wishlist.save()
        return user

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError('Not valid')
        return attrs

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'password2']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        users = User.objects.all()
        user = users.filter(email=email)

        if user:
            authenticated_user = authenticate(username=email, password=password)
            if not authenticated_user:
                raise serializers.ValidationError('Invalid Login Details')
            attrs['user'] = authenticated_user
            return attrs
        else:
            raise serializers.ValidationError('User not registered')
