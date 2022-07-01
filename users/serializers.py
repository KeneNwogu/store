from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Wishlist, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['_id', 'first_name', 'last_name', 'email', 'phone']


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
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
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        users = User.objects.all()
        user = users.filter(email=email)

        if user:
            authenticated_user = authenticate(username=email, password=password)
            print(authenticated_user)
            if not authenticated_user:
                raise serializers.ValidationError('Invalid login details provided')
            attrs['user'] = authenticated_user
            return attrs
        else:
            raise serializers.ValidationError('Invalid email or password')


class UserTransactionSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    reference = serializers.CharField()
    amount = serializers.FloatField()
    description = serializers.CharField()
    transaction_type = serializers.CharField()
    created_at = serializers.DateTimeField()
    paid_at = serializers.DateTimeField()

    def create(self, validated_data):
        Transaction.objects.create(**validated_data)
