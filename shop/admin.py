from django.contrib import admin
from .models import Category, Product, Images
# Register your models here.


def mark_product_as_featured(modeladmin, request, queryset):
    return queryset.update(is_featured=True)


def remove_product_as_featured(modeladmin, request, queryset):
    return queryset.update(is_featured=False)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "is_sale", "is_featured",)
    list_filter = ("is_sale", "is_featured",)
    actions = [mark_product_as_featured, remove_product_as_featured]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
