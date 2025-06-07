from rest_framework import serializers
from .models import *

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "cart_id", "product_id", "quantity")
         
class CartSerializer(serializers.ModelSerializer):
    cartItems = CartItemSerializer(source="cartitem_set", many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ("id", "user_id")
        
class WishListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wishlist
        fields = ("id", "user_id", "product_id")
        
