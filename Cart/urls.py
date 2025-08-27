from django.urls import path
from .views import CartView, CartItemView
from .orderProcess import CreateOrderFromCartView

urlpatterns = [
    path('',CartView.as_view()),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/<int:pk>/', CartItemView.as_view(), name='cart-item'),
    path('cart/item/', CartItemView.as_view(), name='cart-item'),
    path('from-cart/', CreateOrderFromCartView.as_view(), name='create_order_from_cart'),
]
