
from django.urls import path
from carts.views import cart_items, wishlist_views

urlpatterns = [
    path('cart/list', cart_items.CartList.as_view()),
    
    #cart items
    path('cartItem/create', cart_items.CreateCartItem.as_view()),
    path('cartItem/quantity/update/<int:pk>', cart_items.UpdateCartItemQuantity.as_view()),
    path('cartItem/delete/<int:pk>', cart_items.DeleteCartItems.as_view()),
    
    #wishlist
    path('wishList/create', wishlist_views.CreateWishList.as_view()),
    path('wishList/list', wishlist_views.ListWishList.as_view()),
    path('wishList/delete/<int:pk>', wishlist_views.DeleteWishListItems.as_view()),

]
