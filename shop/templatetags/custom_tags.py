from ..models import Product
from django import template
register = template.Library()


def count_products_by_category(category):
    return Product.objects.filter(category=category).count()


register.filter("count_products_by_category", count_products_by_category)
