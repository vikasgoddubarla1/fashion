from users.models import User, UserAddresses
from carts.models import Cart
from rest_framework import generics, status
from rest_framework.response import Response
from users.serializers import UserSerializer, UserListUpdateSerializer, UserRetriveSerializer,UserAddressDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUser(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        Cart.objects.create(
            user_id = user
        )
        
        return Response({"message":"User created successfully!",
                         "userDetails":serializer.data})
        
class UpdateUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListUpdateSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message":"user details updated successfully!", "userDetails":serializer.data})
    

class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListUpdateSerializer
    permission_classes = (IsAuthenticated,)
    
    def list(self, request, *args, **kwargs):
        # if not request.user.is_admin:
        #     return Response({"error":'You do not have permission to perform this action'}, status = 500)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"userDetails":serializer.data})
    
class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetriveSerializer
    permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_admin and not request.user == instance.id:
            return Response({"error":"you do not have permission to perform this action"}, status = 500)
        serializer = self.get_serializer(instance)
        return Response({"userDetails":serializer.data})


class CreateUserAddress(generics.CreateAPIView):
    serializer_class = UserAddressDetailsSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        return Response({"userAddressDetails":serializer.data})
    
class UpdateUserAddress(generics.UpdateAPIView):
    queryset = UserAddresses.objects.all()
    serializer_class = UserAddressDetailsSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"userAddressDetails":serializer.data})
    
class DeleteUserAddress(generics.DestroyAPIView):
    queryset = UserAddresses.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_admin and not request.user.id == instance.user_id.id:
            return Response({"error":'You do not have permission to perform this action'}, status = 500)
        self.perform_destroy(instance)
        return Response({"message":"address deleted successfully!"})
    

class UserLogout(generics.ListAPIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"loggedout successfully!"},status=200)
        except Exception:
            return Response(status=400)