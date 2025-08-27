from rest_framework import serializers
from .models import Order, OrderItem
from Users.serializers import UserSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = UserSerializer(read_only = True)

    class Meta:
        model = Order
        fields = ['id','customer','order_date','total','status','items']