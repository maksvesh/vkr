# main/admin.py
from django.contrib import admin
from .models import Zayavka, UserProfile, Slide

@admin.register(Zayavka)
class ZayavkaAdmin(admin.ModelAdmin):
    list_display = ('user', 'urok', 'data_nachala', 'oplata', 'status', 'sozdana')
    list_filter = ('status', 'urok')
    search_fields = ('user__username', 'urok')
    list_editable = ('status',)
    ordering = ('-sozdana',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'birth_date', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')