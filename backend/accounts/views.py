import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, CreateView
from rest_framework import request
from rest_framework.reverse import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile

def sign_up(request):
    if request.method == 'POST':
        content_type = request.content_type
        if 'application/json' in content_type:
            try:
                body = json.loads(request.body)
                username = body.get('login')
                password = body.get('password')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'})
        else:
            username = request.POST.get('login')
            password = request.POST.get('password')

        if not login or not password:
            return JsonResponse(
                {'error': 'Username and password are required'}
            )
        try:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            Profile.objects.create(user=user)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Registration successful'})
            else:
                return JsonResponse(
                    {'error': 'Authentication failed'}
                )
        except Exception as e:
            return JsonResponse(
                {'error': f'Registration failed: {str(e)}'}
            )
    else:
        return render(request, 'frontend/signUp.html')

def sign_in(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'frontend/signIn.html')

    elif request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']

        if not login or not password:
            messages.error(request, 'Введите имя пользователя и пароль')
            return render(request, 'frontend/signIn.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Редирект на главную страницу
        else:
            return render(request, 'frontend/signIn.html')

def sign_out(request):
    logout(request)
    return redirect('/')

# def sign_up(request: HttpRequest):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             return redirect('/')
#         return render(request, 'frontend/signUp.html')
#
#     elif request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST['password']
#
#         # Проверка обязательных полей
#         if not username or not password:
#             messages.error(request, 'Заполните все поля')
#             return render(request, 'frontend/signUp.html')
#
#         # Проверка существования пользователя
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Пользователь с таким именем уже существует')
#             return render(request, 'frontend/signUp.html')
#
#         try:
#             # Создание пользователя
#             user = User.objects.create_user(
#                 username=username,
#                 password=password
#             )
#             # Автоматическая авторизация после регистрации
#             login(request, user)
#             messages.success(request, 'Регистрация успешна! Добро пожаловать!')
#             return redirect('/')  # Редирект на главную страницу
#
#         except Exception as e:
#             messages.error(request, 'Произошла ошибка при регистрации')
#             return render(request, 'frontend/register.html')
#
#     # Обработка других HTTP-методов
#     return redirect('/')
