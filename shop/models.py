from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField('Опис', blank=True)
    image = models.ImageField('Зображення', upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField('Створено о', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено о', auto_now=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products', verbose_name='Категорія'
    )
    name = models.CharField('Назва', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Опис', blank=True)
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2)
    image = models.ImageField('Фото', upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField('На складі', default=0)
    available = models.BooleanField('Доступний', default=True)
    created_at = models.DateTimeField('Створено о', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено о', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return None


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('processing', 'Обробляється'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='orders', verbose_name='Користувач'
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField('Сума', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('Створено о', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено о', auto_now=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'Замовлення #{self.id} — {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name='Замовлення'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField('Кількість', default=1)
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлень'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    def get_total(self):
        return self.price * self.quantity


class Rating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='ratings', verbose_name='Товар'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='ratings', verbose_name='Користувач'
    )
    score = models.IntegerField(
        'Оцінка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField('Створено о', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено о', auto_now=True)

    class Meta:
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.username} → {self.product.name}: {self.score}/5'


class Newsletter(models.Model):
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Ім\'я', max_length=100, blank=True)
    subscribed_at = models.DateTimeField('Підписався о', auto_now_add=True)

    class Meta:
        verbose_name = 'Підписник'
        verbose_name_plural = 'Підписники'

    def __str__(self):
        return self.email