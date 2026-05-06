from .models import Category


def cart_count(request):
    cart = request.session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return {'cart_count': count}


def categories_menu(request):
    from .models import Category
    return {'categories_menu': Category.objects.all()}