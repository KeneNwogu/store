from rest_framework.serializers import ModelSerializer, JSONField
from .models import Product


class ProductSerializer(ModelSerializer):
    images = JSONField()

    class Meta:
        model = Product
        fields = ['_id', 'name', 'brand', 'description', 'price', 'currency',
                  'in_stock', 'gender', 'images']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
