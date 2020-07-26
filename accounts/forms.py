from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from shop.models import Product

CHOICES = [
    ("is_seller", "Seller"),
    ("is_buyer", "Buyer")
]


class UserRegistrForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1",
                  "password2", "user_type", ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = User.objects.filter(email__iexact=email)
        if is_exist:
            raise forms.ValidationError("A user already exist with that Email")
        return email


# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = BillingAddress
#         fields = ["full_name", "email", "phone", "country",
#                   "city", "state", "zip_code", "address", "is_default"]


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "category", "price", "discount_percentage", "short_description",
                  "long_description", "is_featured", "is_sale", "feature_image"]
