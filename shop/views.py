from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, Category
# Create your views here.


def home(request):
    products = Product.objects.all().order_by('-created_date')
    featured_products = products.filter(is_featured=True)
    saled_products = products.filter(is_sale=True)
    laptops = products.filter(category__name__iexact="Laptop")
    accessories = products.filter(category__name__iexact="accessories")
    mobiles = products.filter(category__name__iexact="mobile")
    watches = products.filter(category__name__iexact="watch")
    context = {
        "products": products,
        "featured_products": featured_products,
        "saled_products": saled_products,
        "laptops": laptops,
        "accessories": accessories,
        "mobiles": mobiles,
        "watches": watches
    }
    return render(request, "shop/index.html", context)


def shop(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(all_products, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        "products": products,
        "categories": categories
    }
    return render(request, "shop/shop.html", context)


def sort_products(request, title):
    data = {}
    products = Product.objects.all().order_by(f"{title}")
    context = {
        "products": products
    }
    data['html'] = render_to_string("snippets/shop-products.html", context)
    return JsonResponse(data, safe=False)


def filter_products(request, name):
    data = {}
    products = Product.objects.filter(category__name__iexact=name)
    context = {
        "products": products
    }
    data['html'] = render_to_string("snippets/shop-products.html", context)
    return JsonResponse(data, safe=False)


def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    same_category_products = Product.objects.filter(
        category=product.category).exclude(id=product.id)
    context = {
        "product": product,
        "products": same_category_products
    }
    return render(request, "shop/product-details.html", context)


def product_details_api(request, id):
    data = {}
    product = Product.objects.get(id=id)
    context = {
        "product": product
    }
    data['html'] = render_to_string(
        "snippets/product-detail-card.html", context)
    return JsonResponse(data, safe=False)
