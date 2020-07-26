from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop", views.shop, name="shop"),
    path("sort-products/<str:title>",
         views.sort_products, name="sort-products"),
    path("filter-products/<str:name>",
         views.filter_products, name="filter-products"),
    path("product-details/<str:slug>",
         views.product_details, name="product-details"),
    path("get-product/<int:id>", views.product_details_api, name="get-product"),


]
