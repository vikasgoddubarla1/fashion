
from django.urls import path
from products.views import product_views, category_views

urlpatterns = [
    path('product/create', product_views.CreateProduct.as_view()),
    path('product/update/<int:pk>', product_views.UpdateProduct.as_view()),
    path('product/retrieve/<int:pk>', product_views.RetrieveProduct.as_view()),
    path('product/list', product_views.ListProduct.as_view()),
    path('product/delete/<int:pk>', product_views.DeleteProduct.as_view()),
    
    path('category/create', category_views.CreateCategory.as_view()),
    path('category/update/<int:pk>', category_views.DeleteCategory.as_view()),
    path('category/list', category_views.ListCategory.as_view()),

]
