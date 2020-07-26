from django.contrib import admin
from .models import Cart, CartItem, WishList, Coupon
# Register your models here.


def activate_coupon(modeladmin, request, queryset):
    return queryset.update(is_active=True)


def deactivate_coupon(modeladmin, request, queryset):
    return queryset.update(is_active=False)


class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "amount", "created_date", "is_active",)
    list_filter = ("is_active")
    actions = [activate_coupon, deactivate_coupon]


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)
admin.site.register(Coupon)
