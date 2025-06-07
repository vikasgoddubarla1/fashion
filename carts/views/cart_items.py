from carts.models import Cart, CartItem
from rest_framework import generics, status
from rest_framework.response import Response
from carts.serializers import CartItemSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated


class CartList(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    
    def queryset(self):
        user = self.request.user
        return Cart.objects.filter(user_id = user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"cartList":serializer.data})
    


#-------------------------------------------------------------- CART ITEMS ----------------------------------------------------------------------
class CreateCartItem(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"cartItemDetails":serializer.data})
    
class UpdateCartItemQuantity(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        quantity = request.data.get("quantity")
        instance = self.get_object()
        instance.quantity = quantity
        instance.save()
        return Response({"cartItemDetails":"quantity updated successfully!"})
    
class DeleteCartItems(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destory(instance)
        return Response({"cartItemDetails":'Cart item deleted successfully!'})