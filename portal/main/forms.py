# main/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label='Имя')
    last_name = forms.CharField(max_length=150, required=True, label='Фамилия')
    patronymic = forms.CharField(max_length=150, required=False, label='Отчество')
    birth_date = forms.DateField(
        required=True, 
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    phone = forms.CharField(max_length=20, required=True, label='Контактный номер телефона')
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': 'Логин',
            'email': 'E-mail',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Проверка: латинские буквы и цифры, минимум 6 символов
        if not re.match(r'^[a-zA-Z0-9]{6,}$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры, длиной минимум 6 символов.')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Проверка: минимум 8 символов
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов.')
        return password

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return birth_date

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Проверка телефона: цифры, пробелы, +, -, скобки
        if not re.match(r'^[\+\d\s\-\(\)]{10,20}$', phone):
            raise forms.ValidationError('Введите корректный номер телефона.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Сохраняем дополнительные поля в профиль
            from .models import UserProfile
            UserProfile.objects.create(
                user=user,
                patronymic=self.cleaned_data.get('patronymic', ''),
                birth_date=self.cleaned_data['birth_date'],
                phone=self.cleaned_data['phone']
            )
        return user