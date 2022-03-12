# from django.contrib import admin
from products.views import ProductDetailsView, ProductListView, CategoriesListView
from django.urls import path

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('<str:pk>/', ProductDetailsView.as_view(), name='product_detail'),
]
