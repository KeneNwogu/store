
from django.urls import path

from retailers.views import CreateProductView, RetailerProductsView, RegisterRetailerView, LoginRetailerView

urlpatterns = [
    path('products/', CreateProductView.as_view(), name='create_product'),
    path('products', RetailerProductsView.as_view(), name='retailer_products'),
    path('register/', RegisterRetailerView.as_view(), name='register_retailer'),
    path('login/', LoginRetailerView.as_view(), name='login_retailer')
]