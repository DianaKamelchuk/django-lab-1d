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
    readonly_fields = ('get_total',)

    def get_total(self, obj):
        if obj.price and obj.quantity:
            return obj.get_total()
        return '-'
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
    list_display = (
        'id', 'first_name', 'last_name', 'phone', 'email',
        'full_address', 'delivery', 'payment',
        'status', 'total_price', 'created_at', 'updated_at'
    )
    list_filter = ('status', 'delivery', 'payment')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'city')
    readonly_fields = ('full_address', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Покупець', {
            'fields': ('user', 'first_name', 'last_name', 'phone', 'email')
        }),
        ('Адреса доставки', {
            'fields': ('country', 'region', 'city', 'street', 'full_address')
        }),
        ('Замовлення', {
            'fields': ('delivery', 'payment', 'comment', 'status', 'total_price')
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def full_address(self, obj):
        parts = [obj.country, obj.region, obj.city, obj.street]
        return ', '.join(p for p in parts if p)
    full_address.short_description = 'Повна адреса'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'score', 'created_at', 'updated_at')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_at')