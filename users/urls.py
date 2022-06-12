# from django.contrib import admin
from users.views import RegisterUserView, UserTokenView, UserListView, UserWishlistView
from django.urls import path

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserTokenView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='users'),
    path('wishlist/', UserWishlistView.as_view(), name='wishlist')
]
