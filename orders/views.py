from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers import OrderItemSerializer, OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        order_items = data.pop('orders')
        order_items_serializer = OrderItemSerializer(data=order_items, many=True)

        if order_items_serializer.is_valid(raise_exception=True):
            # create an order
            total_items = sum([o.get('quantity') for o in order_items_serializer.data])
            total_price = sum([o.get('price') for o in order_items_serializer.data])
            data = {'items': order_items_serializer.data, 'total_items': total_items, 'total_price': total_price}
            order = OrderSerializer(data=data)
            if order.is_valid(raise_exception=True):
                # order.save(user=request.user, products=list(map(lambda x: dict(x), order_items_serializer.data)))
                order.save(user=request.user, products=order_items_serializer.data)
            return Response({'message': 'successfully created order'})
        return Response({'message': 'failed to order items'})


class ViewOrders(generics.ListAPIView):
    # list all orders from user
    def get_queryset(self):
        pass


class ViewOrderDetails(APIView):
    def get(self, request, pk):
        pass
