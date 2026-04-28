from django.shortcuts import render
from .models import Product, Category

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