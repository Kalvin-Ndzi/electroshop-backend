from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, Review, Message
from .serializers import ProductSerializer, ReviewSerializer, TestimonialPostSerializer, ProductUpdateSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from Users.models import User

# Create your views here.
class ProductView(APIView):

    def post(self, request):
        if not hasattr(request.user, 'role') or request.user.role != 'admin':
            return Response({'error': 'Only Admin can create products'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        print("I entered here the prouducts page", request.user)
        products = Product.objects.all()
        print(products)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error':'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)  # ✅


    def put(self,request,pk):
        print(f'updating product now {request.data}')
        if(request.user.role != 'admin'):
            return Response({'error':'Only admin Can update product'})
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductUpdateSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error':'Product Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,pk):
        if request.user.role != 'admin':
            return Response({'error':'Only admins can delete Products'},status=status.HTTP_403_FORBIDDEN)
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'message':'Product deleted succesfully'})
        except Product.DoesNotExist:
            return Response({'error':'Product Not Found'},status=status.HTTP_404_NOT_Found)
        
class ReviewView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user_email = request.user
        user = User.objects.get(email = request.user)

        if user.role != 'buyer':
            return Response({'error':'Only Customers can leave review'}, status=status.HTTP_403_FORBIDDEN)
        print(f'useremail is {user_email}')
        print(f'User is {request.user}')
        print(f'user from email is {user}')
        print(f'trying to get the userid{user.id}, {request.user.id}')

        user_id = request.user.id  
        user = User.objects.get(id = user_id)
        print(f'This is now the user Object after doing all things..{user}')

        testimonial_data = {
            'customer': user.id,
            'message': request.data['message']
        }

        serializer = TestimonialPostSerializer(data=testimonial_data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
class MessagView(APIView):
    def get(self, request):
        user = User.objects.get(email = request.user)
        if user.role != 'admin':
            return Response({"error": "Only admin can see the messages sent here"}, status=status.HTTP_403_FORBIDDEN)
        
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        uemail = request.user
        user = User.objects.get(email = uemail)

        if user.role == 'admin':
            return Response({'error': "Only Buyers can send messages"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['user'] = user.id  

        serializer = MessageSerializer(data=data)
        print(f'this is what you sent {data}')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)