from products.models import Category
from rest_framework import generics, status
from rest_framework.response import Response
from products.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated

class CreateCategory(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(
                {"error": "You do not have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response({"productDetails": serializer.data})
    
class ListCategory(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def list(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"productList":serializer.data})
    
class DeleteCategory(generics.DestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()
        if not request.user.is_admin:
            return Response({"error":"You do not have permission to perform this action"}, status = 500)
        self.perform_destroy(instance)
        return Response({"productDetails":"product deleted successfully!"})
    