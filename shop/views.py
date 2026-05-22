import random
import string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg

from .models import Category, Product, Order, OrderItem, Rating, Newsletter
from .forms import (
    RegisterForm, LoginForm, NewsletterForm, RatingForm,
    PasswordResetRequestForm, PasswordResetConfirmForm, CheckoutForm
)


# ───────────── Головна (Лаба 5) ─────────────
def index(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(available=True)[:8]
    newsletter_form = NewsletterForm()
    return render(request, 'shop/index.html', {
        'categories': categories,
        'featured_products': featured_products,
        'newsletter_form': newsletter_form,
    })


# ───────────── Категорія (Лаба 6) ─────────────
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'shop/category.html', {
        'category': category,
        'products': products,
    })


# ───────────── Товар (Лаба 6) ─────────────
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    avg_rating = product.ratings.aggregate(Avg('score'))['score__avg']
    user_rating = None
    rating_form = RatingForm()

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(product=product, user=request.user).first()
        if user_rating:
            rating_form = RatingForm(instance=user_rating)

    if request.method == 'POST' and 'rate' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        if user_rating:
            form = RatingForm(request.POST, instance=user_rating)
        else:
            form = RatingForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.product = product
            r.user = request.user
            r.save()
            messages.success(request, 'Вашу оцінку збережено!')
            return redirect('product_detail', slug=slug)

    return render(request, 'shop/product.html', {
        'product': product,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'rating_form': rating_form,
        'user_rating': user_rating,
    })


# ───────────── Кошик (Лаба 7) ─────────────
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * item['quantity']
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total': item_total,
            })
        except Product.DoesNotExist:
            pass
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {'quantity': 1}
    request.session['cart'] = cart
    messages.success(request, f'"{product.name}" додано до кошика!')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')


# ───────────── Оформлення замовлення (Лаба 7) ─────────────
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Кошик порожній!')
        return redirect('cart')

    cart_items = []
    total = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * item['quantity']
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total': item_total,
            })
        except Product.DoesNotExist:
            pass

    form = CheckoutForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            phone=form.cleaned_data['phone'],
            email=form.cleaned_data['email'],
            country=form.cleaned_data['country'],
            region=form.cleaned_data['region'],
            city=form.cleaned_data['city'],
            street=form.cleaned_data['street'],
            delivery=form.cleaned_data['delivery'],
            payment=form.cleaned_data['payment'],
            comment=form.cleaned_data['comment'],
            total_price=total,
        )
        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                )
            except Product.DoesNotExist:
                pass

        request.session['cart'] = {}
        messages.success(request, f'Замовлення #{order.id} успішно оформлено!')
        return redirect('order_success')

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    })


def order_success(request):
    return render(request, 'shop/order_success.html')


# ───────────── Розсилка (Лаба 7) ─────────────
def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Дякуємо за підписку!')
            except Exception:
                messages.info(request, 'Цей email вже підписаний.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


# ───────────── Акаунт (Лаба 8) ─────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Реєстрація успішна!')
        return redirect('/')
    return render(request, 'shop/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Ласкаво просимо, {user.username}!')
        return redirect('/')
    return render(request, 'shop/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def account_view(request):
    if request.user.is_staff:
        orders = Order.objects.all().select_related('user').prefetch_related('items__product')
    else:
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'shop/auth/account.html', {'orders': orders})


# ───────────── Скидання паролю (Лаба 8) ─────────────
def password_reset_request(request):
    form = PasswordResetRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
            code = ''.join(random.choices(string.digits, k=6))
            request.session['reset_code'] = code
            request.session['reset_user_id'] = user.id
            send_mail(
                'Відновлення паролю',
                f'Ваш код для відновлення паролю: {code}\n\nКод дійсний 10 хвилин.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            messages.success(request, 'Код надіслано на вашу пошту!')
            return redirect('password_reset_confirm')
        except User.DoesNotExist:
            messages.error(request, 'Користувача з таким email не знайдено.')
    return render(request, 'shop/auth/password_reset.html', {'form': form})


def password_reset_confirm(request):
    form = PasswordResetConfirmForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        code = form.cleaned_data['code']
        new_password = form.cleaned_data['new_password']
        session_code = request.session.get('reset_code')
        user_id = request.session.get('reset_user_id')
        if code == session_code and user_id:
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                del request.session['reset_code']
                del request.session['reset_user_id']
                messages.success(request, 'Пароль успішно змінено! Увійдіть.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Помилка. Спробуйте ще раз.')
        else:
            messages.error(request, 'Невірний код.')
    return render(request, 'shop/auth/password_reset_confirm.html', {'form': form})