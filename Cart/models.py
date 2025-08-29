from django.db import models
from Products.models import Product
from Users.models import User

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='cart')
    number_of_items = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f'{self.product}'