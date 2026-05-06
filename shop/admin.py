from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Rating, Newsletter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price', 'get_total')

    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Сума'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created_at', 'updated_at')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'available')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    inlines = [OrderItemInline]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'score', 'created_at', 'updated_at')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_at')