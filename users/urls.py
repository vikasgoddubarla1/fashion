
from django.urls import path
from users.views import user_views

urlpatterns = [
    path('user/register', user_views.RegisterUser.as_view()),
    path('user/list', user_views.ListUser.as_view()),
    path('user/update/<int:pk>', user_views.UpdateUser.as_view()),
    path('user/retrieve/<int:pk>', user_views.RetrieveUser.as_view()),
    
    #user Address urls
    
    path('user/address/create', user_views.CreateUserAddress.as_view()),
    path('user/address/update/<int:pk>', user_views.UpdateUserAddress.as_view()),
    path('user/address/delete/<int:pk>', user_views.DeleteUserAddress.as_view()),
    
    #logout
    path('user/logout', user_views.UserLogout.as_view()),
    
    
]
