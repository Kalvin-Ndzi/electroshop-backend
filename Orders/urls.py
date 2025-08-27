from django.urls import path
from .views import OrderView, OrderDetailView, GetAllORders

urlpatterns = [
    path('myorders/', OrderView.as_view(), name='process-payment'), 
    path('all_orders/', GetAllORders.as_view()),  
    path('orders/process/', OrderDetailView.as_view(), name='process-order'),
]
