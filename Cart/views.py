from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Cart, CartItem
from rest_framework.permissions import IsAuthenticated
from .serializers import CartItemSerializer, CartSerializer, CartItemSerializerwithProductDetails, CartItemWriteSerializer
from Users.models import User
from django.core.exceptions import ObjectDoesNotExist
from Orders.models import OrderItem
from Orders.serializers import OrderItemSerializer, OrderSerializer
from Orders.models import Order

# Create your views here.
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):

        user = User.objects.get(email=request.user) 
        print("Just coming from this route")
        print(user)
        try:
            cart = Cart.objects.filter(user__email=request.user)
            print(cart)
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error':'Cart not created yet'},status = status.HTTP_404_NOT_FOUND)


    # def post(self, request):
    #     print('getting user email')
    #     try:
    #         # Get user from email
    #         user = User.objects.get(email=request.user)
    #     except ObjectDoesNotExist:
    #         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


    #     if user.role != 'buyer':
    #         return Response({'error': 'Only buyers can add products to cart'}, status=status.HTTP_403_FORBIDDEN)

    #     # Get or create the user's cart
    #     try:
    #         cart = Cart.objects.get(user=user)
    #     except Cart.DoesNotExist:
    #         cart = Cart.objects.create(user=user)

    #     # Validate and create cart item
    #     serializer = CartItemSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(cart=cart)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        print(request.data)
        email = request.user

        user = User.objects.get(email=email)

        if user.role != 'buyer':
            return Response({'error': 'Only buyers can add products to cart'}, status=status.HTTP_403_FORBIDDEN)

        cart, created = Cart.objects.get_or_create(user=user)

        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.permissions import IsAuthenticated  # Uncomment this if needed

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]  # Uncommented for better security

    def put(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk)

            if request.user != item.cart.user:
                return Response({'error': 'You cannot update someone else’s cart'}, status=status.HTTP_403_FORBIDDEN)

            serializer = CartItemWriteSerializer(item, data=request.data)

            if serializer.is_valid():
                serializer.save()

                # Return the full updated item with product details
                full_data = CartItemSerializerwithProductDetails(item)
                return Response(full_data.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self,request):
        email = request.user
        user = User.objects.get(email=email)

        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.all()

        serializer = CartItemSerializerwithProductDetails(cart_items, many=True)
        print(serializer.data)
        return Response(serializer.data)


    def delete(self,request):
        item_id = request.data.get('item_id')
        try:
            item = CartItem.objects.get(pk = item_id)
            if item.cart.user != request.user:
                return Response({'error':'You cannot delete someones item'})
            
            item.delete()
            return Response({'message':'Item Deleted Succesfully'})
        except CartItem.DoesNotExist:
            return Response({'error':'item not found'},status=status.HTTP_404_NOT_FOUND)
