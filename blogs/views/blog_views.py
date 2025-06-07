from blogs.models import Blog
from rest_framework import generics, status
from rest_framework.response import Response
from blogs.serializers import BlogSerializer, BlogListSerializer
from rest_framework.permissions import IsAuthenticated

class CreateBlog(generics.CreateAPIView):
    serializer = BlogSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({"error":"you do not have permission to perform this action"}, status = 500)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response({"blogDetails":'blog created successfully!'})
        
class UpdateBlog(generics.UpdateAPIView):
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({"error":"you do not have permission to perform this action"}, status = 500)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"blogDetails":'blog Updated successfully!'})
    
class ListBlog(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    permission_classes = (IsAuthenticated,)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"blogList":serializer.data})
    
class RetrieveBlog(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"blogList":serializer.data})
    
class DeleteBlog(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({"error":"you do not have permission to perform this action"}, status = 500)
        instance = self.get_object()
        instance.delete()
        return Repsonse({"message":"blog deleted successfully!"})