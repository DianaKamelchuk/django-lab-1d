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