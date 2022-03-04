from bson import ObjectId
from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

# Create your views here.
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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = SmallResultsPagination
