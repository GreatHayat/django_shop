from django.db import models
from decimal import Decimal
from accounts.models import User
from shop.models import Product
# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=10, blank=False,
                            null=False, verbose_name="Coupon Code")
    amount = models.DecimalField(
        max_digits=5, decimal_places=2, blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"


class CartItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="user_cart_products")
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.product}"

    def get_total_price(self):
        if self.product.discount_price:
            return self.quantity * (self.product.price - self.product.discount_price)
        else:
            return self.quantity * self.product.price

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_cart")
    products = models.ManyToManyField(CartItem)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, related_name="cart_coupon", blank=True, null=True)
    total_amount = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    def get_total(self):
        total = 0
        for product in self.products.all():
            total += product.get_total_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def save(self, *args, **kwargs):
        amount = 0
        for product in self.products.all():
            amount += product.get_total_price()
        if self.coupon:
            self.total_amount = amount - self.coupon.amount
        else:
            self.total_amount = amount
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"


class WishList(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wish_product")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_products")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product}"

    class Meta:
        verbose_name = "Wish List"
        verbose_name_plural = "Wish List"
