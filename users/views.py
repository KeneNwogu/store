import datetime

import jwt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from online_shop_be import settings
from products.serializers import ProductSerializer
from utilities.pagination import SmallResultsPagination
from .models import Wishlist
from .serializers import RegistrationSerializer, LoginSerializer


# Create your views here.


class RegisterUserView(APIView):
    def post(self, request):
        user_serializer = RegistrationSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
        return Response({"message": "Successfully created user"})


class UserTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid(raise_exception=True):
            user = login_serializer.validated_data['user']
            # token = Token.objects.get_or_create(user=user)
            user_token_payload = {
                "user_id": str(user._id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=720),
                "iat": datetime.datetime.utcnow()
            }
            token = jwt.encode(user_token_payload, settings.SECRET_KEY, settings.JWT_ENCRYPTION_METHOD)
            return Response({
                'message': 'Successfully created token for user',
                'token': token,
                'user_id': str(user._id),
                'email': user.email
            })


class UserListView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(request.user)
        return Response(request.user.username)


class UserWishlistView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = SmallResultsPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print('user', user)
        wishlist = Wishlist.objects.filter(user=user).first()
        return wishlist.products.all()
