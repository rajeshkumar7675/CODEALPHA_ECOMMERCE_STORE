from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
]
