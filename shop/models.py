import random
import string
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from decimal import Decimal
from ckeditor.fields import RichTextField
from accounts.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False,
                            null=False, verbose_name="Category Name")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    seller = models.ForeignKey(
        User, default=1, on_delete=models.CASCADE, related_name="seller_product")
    title = models.CharField(max_length=100, blank=False,
                             null=False, verbose_name="Product Title")
    slug = models.SlugField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category",
                                 blank=False, null=False, verbose_name="Product Category")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00,
                                blank=False, null=False, verbose_name="Product Price")
    discount_percentage = models.IntegerField(
        blank=True, null=True, help_text="Enter the number for discount percentage like 45", validators=[MinValueValidator(1), MaxValueValidator(100)])
    discount_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00, blank=True, null=True, verbose_name="Discount Price", help_text="Please leave this field as blank it will be filled automatically based on your discount percentage")
    feature_image = models.ImageField(
        upload_to="product_featured_images/", blank=False, null=False, verbose_name="Featured Image")
    short_description = models.TextField(
        verbose_name="Short Description", blank=False, null=False)
    long_description = RichTextField()
    is_featured = models.BooleanField(
        default=False, verbose_name="Featured Product")
    is_sale = models.BooleanField(default=False, verbose_name="On Sale")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def get_discount_price(self):
        return self.price - self.discount_price

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        random_id = ''.join(random.choice(string.digits) for i in range(8))
        self.slug = slugify(self.title+f"-{random_id}")
        if self.discount_percentage:
            self.discount_price = Decimal(
                self.price) / Decimal(100) * Decimal(self.discount_percentage)
            self.is_sale = True
        else:
            self.is_sale = False
        super().save(*args, **kwargs)


class Images(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to="product_images/",
                              verbose_name="Product Image", blank=False, null=False)

    def __str__(self):
        return f"{self.product}"

    class Meta:
        verbose_name = "Image Gallery"
        verbose_name_plural = "Images Gallery"
