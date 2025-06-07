from rest_framework import serializers
from .models import *

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'product_id', 'image')

class ListProductSerializer(serializers.ModelSerializer):
    productImages = ProductImageSerializer(source='productimage_set', many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'sale_price', 'original_price', 'color', 'occasion', 'productImages')
    
class RetrieveProductSerializer(serializers.ModelSerializer):
    productImages = ProductImageSerializer(source='productimage_set', many=True, read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')