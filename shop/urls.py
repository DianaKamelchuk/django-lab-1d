from django.urls import path
from . import views

urlpatterns = [
    # Головна
    path('', views.index, name='index'),

    # Каталог (Лаба 6)
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Кошик (Лаба 7)
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),

    # Розсилка (Лаба 7)
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),

    # Авторизація (Лаба 8)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]