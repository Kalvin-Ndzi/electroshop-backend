from django.urls import path
from .views import PaymentView, ProcessOrder

urlpatterns = [
    path('payments/', PaymentView.as_view(), name='process-payment'),
    path('orders/process/', ProcessOrder.as_view(), name='process-order'),
]
