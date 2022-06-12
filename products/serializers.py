from bson import ObjectId
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, JSONField, ListSerializer, Serializer
from .models import Product


class ProductSerializer(ModelSerializer):
    images = JSONField()
    # brand = serializers.CharField(required=False)
    # description = serializers.CharField(required=False)
    # currency = serializers.CharField(required=False)
    # gender = serializers.CharField(required=False)
    # in_stock = serializers.BooleanField(required=False)
    # name = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ['_id', 'name', 'brand', 'description', 'price', 'currency',
                  'in_stock', 'gender', 'images']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product


class CategorySerializer(Serializer):
    class Meta:
        fields = ['_id', 'type', 'keyword', 'brand', 'count']

    _id = serializers.CharField()
    type = serializers.CharField()
    brand = serializers.CharField(default=None)
    keyword = serializers.CharField(default=None)
    count = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

