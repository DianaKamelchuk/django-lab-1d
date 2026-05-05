from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('category/<int:id>/', views.category_view),
    path('product/<int:id>/', views.product_detail),
    path('add-to-cart/<int:id>/', views.add_to_cart),
    path('rate/<int:id>/', views.add_rating),
    path('cart/', views.cart_view),
]