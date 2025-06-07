from carts.models import Wishlist
from rest_framework import generics, status
from rest_framework.response import Response
from carts.serializers import WishListSerializer
from rest_framework.permissions import IsAuthenticated

class CreateWishList(generics.CreateAPIView):
    serializer_class = WishListSerializer
    permission_class = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        return Response({'wishListDetails':serializer.data})
    
class ListWishList(generics.ListAPIView):
    queryset = Wishlist.objects.all().order_by("-added_at")
    serializer_class = WishListSerializer
    permission_class = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'wishListDetails':serializer.data})
    
class DeleteWishListItems(generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"wishListDetails":'Wish list product deleted successfully!'})