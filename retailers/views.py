import requests
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from online_shop_be.auth import IsRetailer
from online_shop_be import settings
from products.models import Product
from products.serializers import ProductSerializer, ProductDisplaySerializer
from products.views import ProductListView
from retailers.models import Retailer
from retailers.serializers import RetailerRegistrationSerializer, RetailerLoginSerializer
from users.views import RegisterUserView, UserTokenView
from utilities.utils import generate_unique_state_identifier


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


class RegisterRetailerView(RegisterUserView):
    serializer_class = RetailerRegistrationSerializer

    # user state has to be returned for frontend to communicate with sendbox
    def post(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            retailer = user_serializer.save()
            return Response({"message": "Successfully created user", "state": retailer.state_identifier})
        return Response({"message": "Error in transaction", "success": False}, status=400)


class LoginRetailerView(UserTokenView):
    serializer_class = RetailerLoginSerializer


class RetailerAuthenticationView(APIView):
    # user state identifier to get retailer
    # create Token for retailer
    # Generate sendbox access token for retailer
    def get(self, request):
        state = request.args.get('state')
        sendbox_access_key_generation_code = request.args.get('code')

        # verify state and possibly origin of request
        retailer = Retailer.objects.filter(state_identifier=state).first()
        if retailer:
            # TODO: verify if state access key has expired
            # generate sendbox access key
            # reset state
            sendbox_app_id = settings.SENDBOX_APP_ID
            sendbox_secret = settings.SENDBOX_API_SECRET
            redirect_url = settings.SENDBOX_REDIRECT_URL
            sendbox_access_key_generation_url = f"https://sandbox.staging.sendbox.co/oauth/access/access_token?app_id={sendbox_app_id}&redirect_url={redirect_url}&client_secret={sendbox_secret}&code={sendbox_access_key_generation_code}"
            response = requests.get(sendbox_access_key_generation_url)
            data = response.json()
            if response.status_code != 200 or response.status_code != 201:
                return Response({"success": False}, status=response.status_code)
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')
            retailer.access_token = access_token
            retailer.refresh_token = refresh_token
            retailer.state_identifier = generate_unique_state_identifier()
            retailer.save()
        return Response({"success": False, "message": "user could not be identified"}, status=401)


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
