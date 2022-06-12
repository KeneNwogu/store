from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from products.serializers import ProductSerializer
from utilities.pagination import SmallResultsPagination
from .models import User, Wishlist
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.


class RegisterUserView(APIView):
    def post(self, request):
        user_serializer = RegistrationSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
        return Response({"message": "Successfully created user"})


class UserTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid(raise_exception=True):
            user = login_serializer.validated_data['user']
            token = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Successfully created token for user',
                'token': str(token[0]),
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
        wishlist = Wishlist.objects.filter(user=user).first()
        return wishlist.products.all()
