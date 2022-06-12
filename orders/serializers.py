import bson
from bson import ObjectId
from rest_framework import serializers

from orders.models import Order
from products.models import Product


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()
    total = serializers.FloatField()
    price = serializers.FloatField()

    class Meta:
        fields = ['product_id', 'quantity', 'total', 'price']

    def validate(self, attrs):
        product_id = attrs.get('product_id')
        price = attrs.get('price')
        quantity = attrs.get('quantity')
        total = attrs.get('total')

        try:
            product = Product.objects.get(_id=ObjectId(product_id))
        except (bson.errors.InvalidId, Product.DoesNotExist):
            raise serializers.ValidationError('Not valid product')
        else:
            # run sanity checks on orders
            if product.price != price or not product.in_stock or price*quantity != total:
                raise serializers.ValidationError('Invalid product')
            return attrs


class OrderSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField()
    total_price = serializers.FloatField()

    class Meta:
        fields = ['items', 'total']

    def create(self, validated_data):
        # user = self.context['request'].user
        return Order.objects.create(**validated_data)
