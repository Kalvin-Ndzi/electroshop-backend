from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from Orders.models import Order

# Create your views here.
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        #process payment here CALVIN
        payment_method = request.data['payment_method']
        order_id = request.data['order_id']

        try:
            order = Order.objects.get(pk=order_id)
            if order.customer != request.user:
                return Response({'You do not have permission to process this'}, status=status.HTTP_403_FORBIDDEN)
            payment = Payment.objects.create(order=order,payment_method=payment_method)
            #let me try to simulate payment here this is not going to be true
            if payment_method == 'MTN_MOMO':
                #MTN payment logic goes here
                payment.payment_status = 'paid'
                payment.save()
                order.status = 'paid'
                order.save()
                return Response({'message':'payment sucessfully processed'})
            
            #do also for orange Money
            elif payment_method == 'ORANGE_MONEY':
                #Orange payment logic goes here
                payment.payment_status = 'paid'
                payment.save()
                order.status = 'paid'
                order.save()
                return Response({'message':'payment sucessfully processed'})
            #do also for bank transfer
            elif payment_method == 'BANK_TRANSFER':
                #Orange payment logic goes here
                payment.payment_status = 'paid'
                payment.save()
                order.status = 'paid'
                order.save()
                return Response({'message':'payment sucessfully processed'})
            else:
                return Response({'error':'Invalid Payment Method'})
        except Order.DoesNotExist:
            return Response({'error':'Order not Found'}, status=status.HTTP_404_NOT_FOUND)
            

class ProcessOrder(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            order_id = request.data[order_id]
            order = Order.objects.get(order_id)
            if request.user != order.customer:
                return Response({'error':'You canot process someone`s order'}, status=status.HTTP_403_FORBIDDEN)
            #logic here to process order
            order.status = 'processing'
            order.save()
            return Response({'message': 'order processed succesfully'})
        except Order.DoesNotExist:
            return Response({'error':'specified Order does not exist'}, status=status.HTTP_404_NOT_FOUND)