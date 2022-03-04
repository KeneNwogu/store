from rest_framework.serializers import ModelSerializer
from .models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['_id', 'name', 'brand', 'description', 'price', 'currency',
                  'in_stock', 'gender', 'images']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
