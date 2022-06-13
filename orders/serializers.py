import bson
from bson import ObjectId
from rest_framework import serializers

from orders.models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()
    total = serializers.FloatField()
    price = serializers.FloatField()

    class Meta:
        fields = ['product_id', 'quantity', 'total', 'price']

    # def get_default(self):
    #     return OrderItem.objects.filter(_id=ObjectId(self.data.get('_id')))

    def validate(self, attrs):
        product_id = attrs.pop('product_id')
        price = attrs.get('price')
        quantity = attrs.get('quantity')
        total = attrs.get('total')

        try:
            product = Product.objects.get(_id=ObjectId(product_id))
            attrs['product'] = product
        except (bson.errors.InvalidId, Product.DoesNotExist):
            raise serializers.ValidationError('Not valid product')
        else:
            # run sanity checks on orders
            if product.price != price or not product.in_stock or price*quantity != total:
                raise serializers.ValidationError('Invalid product')
            return attrs

    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)


class OrderSerializer(serializers.Serializer):
    _id = serializers.CharField(required=False)
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField()
    total_price = serializers.FloatField()

    class Meta:
        fields = ['_id', 'items', 'total']

    def create(self, validated_data):
        products = validated_data.pop('products')
        validated_data['products'] = [product._id for product in products]
        return Order.objects.create(total_items=validated_data['total_items'],
                                    products_id=validated_data['products'],
                                    total_price=validated_data['total_price'],
                                    user=validated_data['user'])
