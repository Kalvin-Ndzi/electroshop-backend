from rest_framework import serializers
from .models import ShippingAgency, ShippingCost

class ShippingAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAgency
        fields = ['id','name','description']

class ShippingCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCost
        fields = ['id','agency','shipping_cost','order']