from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from Products.models import Product
from Users.models import User
# Create your views here.

class OrderView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'buyer':
            return Response({'error':'Only Customers cn place orders'})
        
        #i create a new order
        order = Order.objects.create(customer=request.user, total=0)
        #add items to the order
        for item in request.data['items']:
            OrderItem.objects.create(order=order, product_id = item['product'], quantity = item['quantity'])
            #update the total
            product = Product.objects.get(id=item['product'])
            order.total +=  item['quantity'] * product.price
        order.save()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def get(self, request):
        
        user = User.objects.get(email = request.user)
        print(user)
        
        if not request.user:
            return Response({"error": "User not Specified"}, status=400)

        orders = Order.objects.filter(customer = user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class GetAllORders(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True) 
        return Response(serializer.data)

    
class OrderDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            order = Order.objects.get(pk=pk)
            if order.customer != request.user and request.user.role != 'admin':
                return Response({'error':'You do not own permissin to see this order'}, status=status.HTTP_403_FORBIDDEN)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error':'Order Not Found'}, status=status.HTTP_404_NOT_FOUND)