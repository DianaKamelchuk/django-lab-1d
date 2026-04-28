from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('category/<int:id>/', views.category_view),
]
path('product/<int:id>/', views.product_detail),