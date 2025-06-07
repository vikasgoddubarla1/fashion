
from django.urls import path
from carts.views import cart_items, wishlist_views

urlpatterns = [
    path('cart/list', cart_items.CartList.as_view()),
]
