from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrForm, AddProductForm

from shop.models import Product
# Create your views here.


def dashboard(request):
    return render(request, "accounts/index.html")


def register(request):
    if request.method == "POST":
        form = UserRegistrForm(request.POST)
        if form.errors:
            messages.error(request, form.errors)
        print(form)
        if form.is_valid():
            print(form)
            form.save()
    else:
        form = UserRegistrForm()
    context = {
        "form": UserRegistrForm()
    }
    return render(request, "accounts/register.html", context)


def add_new_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect("user-products")
    else:
        form = AddProductForm()
    context = {
        "form": form
    }
    return render(request, "accounts/add-product.html", context)


def user_products(request):
    products = Product.objects.filter(seller=request.user)
    context = {
        "products": products
    }
    return render(request, "accounts/user-products.html", context)


def user_product_details(request, slug):
    product = Product.objects.get(seller=request.user, slug=slug)
    context = {
        'product': product
    }
    return render(request, "accounts/user-product-details.html", context)


def delete_user_product(request, slug):
    product = Product.objects.get(seller=request.user, slug=slug)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("user-products")
