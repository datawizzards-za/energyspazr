from rest_framework import serializers
from app import models


class ProductBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductBrand
        fields = ['id', 'name', 'product']

class OrderDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Order
        fields = ['client', 'date', 'order_number']

class SystemOrderDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.SystemOrder
        fields = ['need_finance', 'include_installation', 'order_number']

class ClientSerializer(serializers.ModelSerializer):
    #physical_address = serializers.StringRelatedField(many=False);
    
    class Meta:
        model = models.Client
        fields = ['id','username', 'lastname', 'firstname', 
        'contact_number'] #, 'building_name', 'street_name']
    

