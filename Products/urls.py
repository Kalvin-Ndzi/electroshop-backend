from django.urls import path
from .views import ProductDetailView, ProductView, ReviewView, MessagView

urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-details'),
    path('reviews/', ReviewView.as_view()),
    path('message', MessagView.as_view()),
]
