from django.urls import path
from .views import shippingAgencyView, ShippingAgencyDetailView

urlpatterns = [
    path('shipping/', shippingAgencyView.as_view(), name='process-payment'),     # Handle payment
    path('orders/process/', ShippingAgencyDetailView.as_view(), name='process-order'), # Simulate order processing
]
