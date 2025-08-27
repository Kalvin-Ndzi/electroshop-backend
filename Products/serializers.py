from rest_framework import serializers
from .models import Product, Review, Message
from Users.serializers import UserSerializer
from Users.models import User

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url = True)

    class Meta:
        model = Product
        fields = ['id','title','price','description','created_by','created_at','image']


class ProductUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'created_by', 'created_at', 'image']
        read_only_fields = ['id', 'created_by', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only = True)
    
    class Meta:
        model = Review
        fields = ['id','customer','message','created_at']

class TestimonialPostSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only = True)

    class Meta:
        model = Review
        fields = ['id','customer','message']

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Message
        fields = ['id', 'user', 'message']
        read_only_fields = ['id']