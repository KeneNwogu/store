import os

from cloudinary import uploader, exceptions
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from online_shop_be.settings import ALLOWED_EXTENSIONS
from users.models import User
from users.serializers import UserSerializer
from .models import Product


class ProductSerializer(ModelSerializer):
    # images = JSONField()
    images = serializers.ListField(default=[])
    rating = serializers.IntegerField(required=False, default=None)
    quantity = serializers.IntegerField(required=False, default=10)
    retailer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # serializer_related_field = User

    class Meta:
        model = Product
        fields = ['_id', 'name', 'brand', 'description', 'price', 'currency',
                  'in_stock', 'gender', 'images', 'rating', 'quantity', 'retailer']

    def create(self, validated_data):
        if not validated_data.get('retailer'):
            raise serializers.ValidationError('No user')

        # validated_data['retailer'] = UserSerializer(read_only=True)
        images = validated_data.pop('images')
        image_urls = []

        for image in images:
            if image == '':
                raise serializers.ValidationError('Invalid image was provided')
            _, ext = os.path.splitext(image.name)
            if ext.lower() not in ALLOWED_EXTENSIONS:
                raise serializers.ValidationError('Invalid image was provided')
            try:
                image_url = uploader.upload(image).get('url')
            except exceptions.Error:
                raise serializers.ValidationError('Failed to upload to cloudinary')
            image_urls.append(image_url)
        validated_data['images'] = image_urls
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


class ProductDisplaySerializer(ProductSerializer):
    retailer = UserSerializer()