from django.db import models
from Products.models import Product
from Users.models import User
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    # order_date = models.DateField(auto_now_add=True)
    order_date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=(
        ('pending','Pending'),
        ('shipped','Shipped'),
        ('deliverd','Deliverd')
    ), default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    quantity = models.IntegerField()