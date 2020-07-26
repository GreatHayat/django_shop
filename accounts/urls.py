from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register", views.register, name="register"),
    path("login", LoginView.as_view(
        template_name="accounts/login.html"), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    # path("profile", views.user_profile, name="profile"),
    # path("add-new-address", views.add_new_address, name="add-new-address"),
    # path("address-book", views.user_address_book, name="address-book"),
    # path("my-orders", views.user_orders, name="my-orders"),

    path("add-new-product", views.add_new_product, name="add-new-product"),
    path("user-products", views.user_products, name="user-products"),
    path("my-product-details/<str:slug>",
         views.user_product_details, name="my-product-details"),
    path("delete-user-product/<str:slug>",
         views.delete_user_product, name="delete-user-product")
]
