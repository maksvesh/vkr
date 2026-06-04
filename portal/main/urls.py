from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.vyhod, name='logout'),
    path('kabinet/', views.kabinet, name='kabinet'),
    path('zayavka/', views.zayavka_new, name='zayavka_new'),
    path('otzyv/<int:pk>/', views.otzyv, name='otzyv'),
]
