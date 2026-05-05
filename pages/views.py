from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import Product, Category, Cart, Rating


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'pages/home.html', {
        'products': products,
        'categories': categories
    })


def category_view(request, id):
    products = Product.objects.filter(category_id=id)
    categories = Category.objects.all()

    return render(request, 'pages/category.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()

    avg_rating = Rating.objects.filter(product=product).aggregate(Avg('value'))['value__avg']

    return render(request, 'pages/product.html', {
        'product': product,
        'categories': categories,
        'avg_rating': avg_rating
    })


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    Cart.objects.create(product=product)

    return redirect('/')


def cart_view(request):
    items = Cart.objects.all()
    categories = Category.objects.all()

    return render(request, 'pages/cart.html', {
        'items': items,
        'categories': categories
    })


def add_rating(request, id):
    if request.method == 'POST':
        value = int(request.POST.get('rating', 0))

        if value < 1 or value > 5:
            value = 0

        product = get_object_or_404(Product, id=id)

        Rating.objects.create(product=product, value=value)

    return redirect(f'/product/{id}/')