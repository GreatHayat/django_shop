from django.test import TestCase
from django.urls import reverse, resolve
from .models import Category, Attribute, Product
from . import views
# Create your tests here.


class ShopModelsTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Test")
        attribute = Attribute.objects.create(name="Color", value="Red")
        product = Product.objects.create(title="Test Title", category=category,
                                         price=35.99, description="Test Description")
        product.attributes.add(attribute)
        product.save()

    def test_category_str_equalto_name(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.__str__(), category.name)

    def test_attribute_str_equalto_name(self):
        attr = Attribute.objects.get(id=1)
        self.assertEqual(str(attr), f"{attr.name} - {attr.value}")

    def test_product_str_equalto_title(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.__str__(), product.title)

    def test_category_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Category Name")

    def test_category_name_length(self):
        category = Category.objects.get(id=1)
        max_len = category._meta.get_field("name").max_length
        self.assertEqual(max_len, 50)

    def test_attribute_name_field_label(self):
        attribute = Attribute.objects.get(id=1)
        field_label = attribute._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Attribute Name")

    def test_attribute_value_field_label(self):
        attribute = Attribute.objects.get(id=1)
        field_label = attribute._meta.get_field("value").verbose_name
        self.assertEqual(field_label, "Attribute Value")

    def test_attirbute_name_length(self):
        attirbute = Attribute.objects.get(id=1)
        max_len = attirbute._meta.get_field("name").max_length
        self.assertEqual(max_len, 30)

    def test_attirbute_value_length(self):
        attirbute = Attribute.objects.get(id=1)
        max_len = attirbute._meta.get_field("value").max_length
        self.assertEqual(max_len, 30)

    def test_product_field_labels(self):
        product = Product.objects.get(id=1)
        title_field = product._meta.get_field("title").verbose_name
        category_field = product._meta.get_field("category").verbose_name
        attribute_field = product._meta.get_field("attributes").verbose_name
        price_field = product._meta.get_field("price").verbose_name
        discount_price_field = product._meta.get_field(
            "discount_price").verbose_name
        featured_image_field = product._meta.get_field(
            "feature_image").verbose_name
        description_field = product._meta.get_field("description").verbose_name
        self.assertEqual(title_field, 'Product Title')
        self.assertEqual(category_field, "Product Category")
        self.assertEqual(attribute_field, "Product Attributes")
        self.assertEqual(price_field, "Product Price")
        self.assertEqual(discount_price_field, "Discount Price")
        self.assertEqual(featured_image_field, "Featured Image")
        self.assertEqual(description_field, "Product Description")

    def test_product_title_length(self):
        product = Product.objects.get(id=1)
        max_len = product._meta.get_field("title").max_length
        self.assertEqual(max_len, 100)

    def test_product_price_max_digits(self):
        product = Product.objects.get(id=1)
        max_digits = product._meta.get_field("price").max_digits
        self.assertEqual(max_digits, 6)


class ShopViewTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolve_home_view(self):
        view = resolve("/")
        self.assertEqual(view.func, views.home)


# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# # from .models import BillingAddress
# # from .forms import UserRegistrForm, AddressForm
# from cart.models import Cart
# # Create your views here.


# def dashboard(request):
#     return render(request, "accounts/dashboard.html")


# def user_profile(request):
#     user = User.objects.get(username=request.user.username)
#     context = {
#         "user": user
#     }
#     return render(request, "accounts/profile.html", context)


# def user_address_book(request):
#     billing = BillingAddress.objects.filter(user=request.user)
#     context = {
#         "billing": billing
#     }
#     return render(request, 'accounts/address-book.html', context)


# def user_orders(request):
#     user_cart = Cart.objects.get(user=request.user)
#     context = {
#         "orders": user_cart.products.all()
#     }
#     return render(request, "accounts/user-orders.html", context)
#     # except Cart.DoesNotExist:
#     #     return render(request, "accounts/user-orders.html")


# def add_new_address(request):
#     if request.method == "POST":
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             billing = form.save(commit=False)
#             billing.user = request.user
#             billing.save()
#             messages.success(
#                 request, "Address Added to your book successfully")
#             return redirect("address-book")
#     else:
#         form = AddressForm()

#     context = {
#         "form": form
#     }

#     return render(request, "accounts/add-address.html", context)


# def register(request):
#     if request.method == "POST":
#         form = UserRegistrForm(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, "Account has been created successfully, Please login with your credentials")
#             return redirect("login")
#     else:
#         form = UserRegistrForm()

#     context = {
#         "form": form
#     }
#     return render(request, "accounts/register.html", context)
