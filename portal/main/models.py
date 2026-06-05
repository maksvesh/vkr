# main/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    patronymic = models.CharField(max_length=150, blank=True, verbose_name='Отчество')
    birth_date = models.DateField(verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль: {self.user.username}'
    
    def get_full_name(self):
        if self.patronymic:
            return f'{self.user.last_name} {self.user.first_name} {self.patronymic}'
        return f'{self.user.last_name} {self.user.first_name}'

class Slide(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=500, verbose_name='Подзаголовок', blank=True)
    image = models.ImageField(upload_to='slides/', verbose_name='Изображение')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title

class Zayavka(models.Model):
    STATUS = [
        ('novaya', 'Новая'),
        ('v-rabote', 'Идет обучение'),
        ('zavershena', 'Обучение завершено'),
    ]
    
    OPLATA_CHOICES = [
        ('nalichnie', 'Наличные'),
        ('karta', 'Банковская карта'),
        ('online', 'Онлайн-оплата'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    urok = models.CharField(max_length=100, verbose_name='Урок')
    data_nachala = models.DateField(verbose_name='Дата начала')
    oplata = models.CharField(max_length=50, choices=OPLATA_CHOICES, verbose_name='Способ оплаты')
    status = models.CharField(max_length=20, choices=STATUS, default='novaya', verbose_name='Статус')
    otzyv = models.TextField(blank=True, verbose_name='Отзыв')
    sozdana = models.DateTimeField(auto_now_add=True, verbose_name='Создана')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-sozdana']

    def __str__(self):
        return f'{self.user.username} — {self.urok} ({self.get_status_display()})'