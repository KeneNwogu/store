from bson import ObjectId
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductSerializer, CategorySerializer
# Create your views here.
from utilities.database import categories
from utilities.pagination import SmallResultsPagination


class ProductDetailsView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(_id=ObjectId(pk))
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductSerializer(product)
            return Response(serializer.data)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
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


class CategoriesListView(APIView):
    def get(self, request):
        category_list = list(categories.find())
        # print(category_list)
        serializer = CategorySerializer(category_list, many=True)
        return Response(serializer.data)
