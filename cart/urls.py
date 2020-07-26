from django.urls import path
from . import views

urlpatterns = [
    path("", views.shopping_cart, name="cart"),
    path('add-to-cart/<str:slug>', views.add_to_cart, name="add-to-cart"),
    path("add-to-wishlist/<int:id>", views.add_to_wishlist, name="add-to-wishlist"),
    path("remove-cart-product/<str:slug>",
         views.remove_cart_product, name="remove-cart-product"),
    path("apply-coupon", views.apply_coupon, name="apply-coupon")
]
