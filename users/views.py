import datetime

import jwt
import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from online_shop_be import settings
from orders.models import Order
from products.serializers import ProductSerializer
from utilities.pagination import SmallResultsPagination
from .models import Wishlist, User
from .serializers import RegistrationSerializer, LoginSerializer, UserTransactionSerializer


# Create your views here.


class RegisterUserView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
        return Response({"message": "Successfully created user"})


class UserTokenView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data)
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
        wishlist = Wishlist.objects.filter(user=user).first()
        return wishlist.products.all()


class UserTransactionWebHook(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.get('data', {})
        transaction_reference = data.get('reference')
        amount = data.get('amount', 0)
        customer = data.get('customer')
        customer_email = customer.get('email')
        paid_at = data.get('paid_at')
        created_at = data.get('created_at')

        if data.get('status') != 'success':
            return Response({'success': False}, status=400)

        # TODO verify transaction reference
        paystack_verification_url = f'https://api.paystack.co/transaction/verify/{transaction_reference}'
        headers = {
            'Authorization': 'Bearer ' + settings.PAYSTACK_SECRET_KEY
        }
        response = requests.get(url=paystack_verification_url, headers=headers)
        response_data = response.json()
        verification_data = response_data.get('data')
        verification_customer = verification_data.get('customer', {})
        verification_customer_email = verification_customer.get('email')
        if verification_data.get('status') != 'success' or amount < verification_data.get('amount') or \
                verification_customer_email != customer_email:
            return Response({'success': False}, status=400)

        order = Order.objects.filter(reference=transaction_reference).first()
        user = User.objects.filter(email=customer_email).first()
        if order and user:
            if amount >= order.total_price:
                transaction_data = {
                    'user': user._id,
                    'reference': transaction_reference,
                    'amount': amount,
                    'description': "Order Checkout",
                    'transaction_type': "dr",
                    'created_at': created_at,
                    'paid_at': paid_at
                }
                transaction = UserTransactionSerializer(data=transaction_data)
                if transaction.is_valid():
                    order.paid = True
                    order.processed_at = datetime.datetime.utcnow()
                    order.save()
                    transaction.save()
                    return Response({'success': True})
        return Response({'success': False}, status=400)
