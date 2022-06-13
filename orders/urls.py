from django.urls import path

from orders.views import CreateOrderView, ViewOrders, ViewOrderDetails

urlpatterns = [
    path('', CreateOrderView.as_view(), name='create_order'),
    path('my-orders/', ViewOrders.as_view(), name='user_orders'),
    path('<str:pk>/order/', ViewOrderDetails.as_view(), name='order_details')
]
