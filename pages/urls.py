from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('<str:page_id>/', views.dynamic_page, name='dynamic_page'),
]