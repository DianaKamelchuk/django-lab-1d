from django.contrib import admin
from .models import Category, Product, Order, Cart, Subscriber, Rating

# вже є
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at', 'updated_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'customer_name', 'created_at', 'updated_at')

admin.site.register(Cart)
admin.site.register(Subscriber)
admin.site.register(Rating)