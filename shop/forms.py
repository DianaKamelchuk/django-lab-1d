from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Newsletter, Rating


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email', 'name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Ваш email'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ваше ім\'я'}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('score',)
        widgets = {
            'score': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)])
        }


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Ваш email'})
    )


class PasswordResetConfirmForm(forms.Form):
    code = forms.CharField(
        label='Код підтвердження',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    new_password = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    confirm_password = forms.CharField(
        label='Підтвердити пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password') != cleaned.get('confirm_password'):
            raise forms.ValidationError('Паролі не співпадають')
        return cleaned


class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        label="Ім'я", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Ім'я *"})
    )
    last_name = forms.CharField(
        label='Прізвище', max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Прізвище *'})
    )
    phone = forms.CharField(
        label='Телефон', max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Телефон * (наприклад: +380991234567)',
            'pattern': '[+0-9]{10,15}',
            'title': 'Введіть номер телефону цифрами (10-15 цифр)',
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email *'})
    )
    country = forms.CharField(
        label='Країна', max_length=100, initial='Україна',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Країна *'})
    )
    region = forms.CharField(
        label='Область', max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Область *'})
    )
    city = forms.CharField(
        label='Місто', max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Місто *'})
    )
    street = forms.CharField(
        label='Вулиця, будинок, квартира', max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Вулиця, будинок, квартира *'})
    )
    delivery = forms.ChoiceField(
        label='Спосіб доставки',
        choices=[
            ('nova_poshta', 'Нова Пошта'),
            ('ukrposhta', 'Укрпошта'),
            ('self_pickup', 'Самовивіз'),
        ],
        widget=forms.RadioSelect()
    )
    payment = forms.ChoiceField(
        label='Спосіб оплати',
        choices=[
            ('online', 'Оплата онлайн'),
            ('cod', 'Накладеним платежем'),
            ('parts', 'Оплата частинами'),
        ],
        widget=forms.RadioSelect()
    )
    comment = forms.CharField(
        label='Коментар',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Коментар до замовлення...'})
    )
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned = phone.replace('+', '').replace(' ', '').replace('-', '')
        if not cleaned.isdigit():
            raise forms.ValidationError('Телефон може містити лише цифри та символ +')
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise forms.ValidationError('Телефон має містити від 10 до 15 цифр')
        return phone