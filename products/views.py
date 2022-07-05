from bson import ObjectId
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from products.serializers import ProductSerializer, CategorySerializer, ProductDisplaySerializer
# Create your views here.
from users.models import Wishlist
from utilities.database import categories
from utilities.pagination import SmallResultsPagination


class ProductDetailsView(APIView):
    authentication_classes = []

    @method_decorator(cache_page(60 * 60 * 12))
    @method_decorator(vary_on_cookie)
    def get(self, request, pk):
        try:
            product = Product.objects.get(_id=ObjectId(pk))
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductSerializer(product)
            return Response(serializer.data)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductDisplaySerializer
    pagination_class = SmallResultsPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['brand', 'gender']
    search_fields = ['description']

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(gender=category) or queryset.filter(brand=category)
        return queryset

    @method_decorator(cache_page(60 * 60 * 8))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(self.request, *args, **kwargs)


class CategoriesListView(APIView):
    @method_decorator(cache_page(60 * 60 * 8))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        category_list = list(categories.find())
        serializer = CategorySerializer(category_list, many=True)
        return Response(serializer.data)


class ProductWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        wishlist = Wishlist.objects.filter(user=user)
        if not wishlist.exists():
            Wishlist(user=user).save()
        wishlist = wishlist.first()
        product = Product.objects.get(_id=ObjectId(pk))
        wishlist.products.add(product)
        return Response({'message': 'succesfully added product to wishlist'})

