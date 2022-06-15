from bson import ObjectId
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from orders.models import Order
from orders.serializers import OrderItemSerializer, OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        order_items = data.pop('orders')
        order_items_serializer = OrderItemSerializer(data=order_items, many=True)

        if order_items_serializer.is_valid(raise_exception=True):
            # create an order
            items = order_items_serializer.save()
            total_items = sum([o.get('quantity') for o in order_items_serializer.data])
            total_price = sum([o.get('price') for o in order_items_serializer.data])
            data = {'items': order_items_serializer.data, 'total_items': total_items, 'total_price': total_price}
            order = OrderSerializer(data=data)
            if order.is_valid(raise_exception=True):
                # order.save(user=request.user, products=list(map(lambda x: dict(x), order_items_serializer.data)))
                order.save(user=request.user, products=items)
            return Response({'message': 'successfully created order'})
        return Response({'message': 'failed to order items'})


class ViewOrders(APIView):
    # list all orders from user
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(data=orders.all(), many=True)
        serializer.is_valid()
        return Response(serializer.data)


class ViewOrderDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = Order.objects.get(_id=ObjectId(pk))
        serializer = OrderItemSerializer(data=order.products.all(), many=True)
        serializer.is_valid()
        return Response(serializer.data)
