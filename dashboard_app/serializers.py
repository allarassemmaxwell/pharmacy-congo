from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import *

User = get_user_model()









class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
        	'id',
        	'category',
        	'stock',
        	'name',
        	'unity_price',
        	'quantity',
        	'discount',
        	'image',
        	'brand_name',
        	'genetic_name',
        	'description',
        	'active',
        	'timestamp',
        	'updated',
        	'slug' 
        ]
        read_only_fields = ['id', 'timestamp', 'updated', 'category', 'stock']









class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
        	'id',
        	'product', 
        	'quantity',
        	'unity_price'
        	'total'
        	'recu'
        	'active',
        	'timestamp', 
        	'updated',
        ]
        read_only_fields = ['id', 'timestamp', 'updated']















