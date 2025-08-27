from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from Orders.models import Order, OrderItem
from Orders.serializers import OrderSerializer

class CreateOrderFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role != 'buyer':
            return Response({'error': 'Only buyers can place orders'}, status=status.HTTP_403_FORBIDDEN)

        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()

            if not cart_items.exists():
                return Response({'error': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.create(customer=user, total=0)
            total = 0

            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                total += item.quantity * item.product.price

            order.total = total
            order.save()

            # Delete all cart items
            cart_items.delete()

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
