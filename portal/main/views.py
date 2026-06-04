# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Zayavka,Slide
from .forms import CustomUserCreationForm

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('kabinet')
    else:
        form = AuthenticationForm()
    return render(request, 'main/home.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('kabinet')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def vyhod(request):
    logout(request)
    return redirect('home')

@login_required
def kabinet(request):
    zayavki = Zayavka.objects.filter(user=request.user)
    slides = Slide.objects.filter(is_active=True) 
    return render(request, 'main/kabinet.html', {
        'zayavki': zayavki,
        'slides': slides
    })

@login_required
def zayavka_new(request):
    error = None
    if request.method == 'POST':
        urok = request.POST.get('urok', '').strip()
        data_nachala = request.POST.get('data_nachala', '').strip()
        oplata = request.POST.get('oplata', '').strip()
        if urok and data_nachala and oplata:
            from datetime import datetime
            Zayavka.objects.create(
                user=request.user,
                urok=urok,
                data_nachala=datetime.strptime(data_nachala, '%Y-%m-%d').date(),
                oplata=oplata,
            )
            return redirect('kabinet')
        else:
            error = 'Пожалуйста, заполните все поля.'
    return render(request, 'main/zayavka.html', {'error': error})

@login_required
def otzyv(request, pk):
    zayavka = get_object_or_404(Zayavka, pk=pk, user=request.user, status='zavershena')
    if request.method == 'POST':
        tekst = request.POST.get('otzyv', '').strip()
        if tekst:
            zayavka.otzyv = tekst
            zayavka.save()
            return redirect('kabinet')
    return render(request, 'main/otzyv.html', {'zayavka': zayavka})