from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ShippingAgency
from .serializers import ShippingAgencySerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class shippingAgencyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'admin':
            return Response({'error':'Only Admin can create Shipping Agencies'})
        serializer = ShippingAgencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ShippingAgencyDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            agency = ShippingAgency.objects.get(pk=pk)
            serializer = ShippingAgencySerializer(agency)
            return Response(serializer.data)
        except ShippingAgency.DoesNotExist:
            return Response({'error':'Shipping Agency Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,pk):
        if request.user.role != 'admin':
            return Response({'error':'Only Admin can update shipping agencies'})
        try:
            agency = ShippingAgency.objects.get(pk=pk)
            serializer = ShippingAgencySerializer(agency, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'error':'Shipping Agency not found'}, status=status.HTTP_400_BAD_REQUEST)
        except ShippingAgency.DoesNotExist:
            return Response({'error':'Shipping Agency Not Found'}, status= status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        if request.user.role != 'admin':
            return Response({'error':'Only admin can delete an agency'})
        try:
            agency = ShippingAgency.objects.get(pk=pk)
            agency.delete()
            return Response({'message':'Agency has been deleted'})
        except ShippingAgency.DoesNotExist:
            return Response({'error':'Shiping agency is not registerd'}, status=status.HTTP_404_NOT_FOUND)
        
