from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from online_shop_be.auth import IsRetailer
from products.models import Product
from products.serializers import ProductSerializer, ProductDisplaySerializer
from products.views import ProductListView
from retailers.serializers import RetailerRegistrationSerializer, RetailerLoginSerializer
from users.views import RegisterUserView, UserTokenView


class CreateProductView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsRetailer]

    def post(self, request):
        data = request.data
        data['retailer'] = self.request.user._id
        # print('user valid', data['retailer'].is_valid(raise_exception=True))
        product_serializer = ProductSerializer(data=data)
        if product_serializer.is_valid(raise_exception=True):
            print(product_serializer.validated_data)
            product_serializer.save()
        return Response({'message': 'successfully added product'})


class RegisterRetailerView(APIView):
    serializer_class = RetailerRegistrationSerializer
    # create retailer profile
    def post(self):
        pass

class LoginRetailerView(UserTokenView):
    serializer_class = RetailerLoginSerializer


class RetailerAuthenticationView(APIView):
    def get(self):
        pass

    def post(self):
        pass


class RetailerProductsView(ProductListView):
    serializer_class = ProductDisplaySerializer
    permission_classes = [IsRetailer]

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(retailer=user).all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(gender=category) or queryset.filter(brand=category)
        return queryset
