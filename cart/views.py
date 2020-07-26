from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import Cart, CartItem, WishList, Coupon
from shop.models import Product
# Create your views here.


def shopping_cart(request):
    cart = Cart.objects.get(user=request.user)
    context = {
        "cart": cart
    }
    return render(request, "cart/shopping-cart.html", context)


def add_to_cart(request, slug):
    data = {}
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        product = get_object_or_404(Product, slug=slug)
        order_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, ordered=False)
        cart_qs = Cart.objects.filter(user=request.user, ordered=False)
        if cart_qs.exists():
            cart_product = cart_qs[0]
            if cart_product.products.filter(product__slug=product.slug).exists():
                order_item.quantity += int(quantity)
                order_item.save()
                data['message'] = "Item added to the cart successfully with quantity increased"
                data['total_price'] = request.user.user_cart.get().get_total()
                data['counter'] = cart_product.products.count()
                return JsonResponse(data)
            else:
                cart_product.products.add(order_item)
                context = {
                    "order_item": order_item,
                }
                data['html'] = render_to_string(
                    "cart/cart-item.html", context, request=request)
                data['counter'] = cart_product.products.count()
                data['total_price'] = request.user.user_cart.get().get_total()
                data['message'] = "Item added to the cart successfully!"
                return JsonResponse(data)
        else:
            cart = Cart.objects.create(user=request.user)
            cart.products.add(order_item)
            return JsonResponse({"message": "Item added to your cart with creation of CART"})


def remove_cart_product(request, slug):
    data = {}
    product = get_object_or_404(Product, slug=slug)
    cart_qs = Cart.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.products.filter(product__slug=product.slug).exists():
            cart_item = CartItem.objects.get(
                user=request.user, product=product, ordered=False)
            cart.products.remove(cart_item)
            cart_item.delete()
            data['message'] = "Item removed from the cart"
            data['counter'] = cart.products.count()
            data['total_price'] = request.user.user_cart.get().get_total()
    return JsonResponse(data)


def apply_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")
        print(coupon_code)
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            user_cart = Cart.objects.get(user=request.user, ordered=False)
            if user_cart.coupon == coupon:
                return JsonResponse({"message": "You already have used this coupon"})
            else:
                user_cart.coupon = coupon
                user_cart.save()
                return JsonResponse({"success": f"You have received ${coupon.amount} discount on your shopping!", "total": user_cart.total_amount})
        except Coupon.DoesNotExist:
            return JsonResponse({"message": "Invalid Coupon Code"})


def product_feedback(request, slug):
    data = {}
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        review = request.POST.get("review")
        name = request.POST.get("name")
        email = request.POST.get("email")
        rating = request.POST.get("rating")
        review = Review.objects.create(
            user=request.user,
            product=product,
            name=name,
            email=email,
            message=review,
            rating=rating
        )
        context = {
            "review": review
        }
        data['html'] = render_to_string("snippets/review.html", context)
        return JsonResponse(data)


def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)
    WishList.objects.create(product=product, user=request.user)
    wishlist_counter = WishList.objects.filter(user=request.user).count()
    return JsonResponse({"message": "Item added to wishlist successfully!", "counter": wishlist_counter})
