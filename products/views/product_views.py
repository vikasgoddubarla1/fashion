from products.models import Product, ProductImage
from rest_framework import generics, status
from rest_framework.response import Response
from products.serializers import ProductSerializer, ListProductSerializer, RetrieveProductSerializer
from rest_framework.permissions import IsAuthenticated

class CreateProduct(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # if not request.user.is_admin:
        #     return Response(
        #         {"error": "You do not have permission to perform this action"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        product_files = request.FILES.getlist('files')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()  # this returns the created Product instance

        for product_file in product_files:
            ProductImage.objects.create(
                product_id=product,
                image=product_file
            )

        return Response({"productDetails": serializer.data})
    
class UpdateProduct(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({"error":"you do not have permission to perform this action"}, status = 500)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"productDetails":serializer.data})
    
class ListProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"productList":serializer.data})
    
class DeleteProduct(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_admin:
            return Response({"error":"You do not have permission to perform this action"}, status = 500)
        self.perform_destroy(instance)
        return Response({"productDetails":"product deleted successfully!"})
    
class RetrieveProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = RetrieveProductSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"productDetails":serializer.data})