import json
import os
import uuid

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from jsonschema import ValidationError
from rest_framework.parsers import MultiPartParser

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import ProfileSerializer
from .models import Profile
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')

        if not user.check_password(current_password):
            return Response(
                {'error': 'Current password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        return Response({'status': 'Password updated'}, status=status.HTTP_200_OK)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        data = request.data

        if 'email' in data:
            user.email = data['email']
        if 'phone' in data:
            user.phone = data['phone']

        try:
            user.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        profile, created = Profile.objects.get_or_create(user=user)
        profile_serializer = ProfileSerializer(profile, data=data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        return self.put(request)

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
                return redirect('/')
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
            return redirect('/')
        else:
            return render(request, 'frontend/signIn.html')


def sign_out(request):
    logout(request)
    return redirect('/')

class ProfileUpdateAvatar(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            profile, created = Profile.objects.get_or_create(user=request.user)

            if 'avatar' not in request.FILES:
                return Response(
                    {'error': 'No avatar file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            avatar_file = request.FILES['avatar']

            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            file_ext = os.path.splitext(avatar_file.name)[1].lower()
            if file_ext not in valid_extensions:
                return Response(
                    {'error': 'Unsupported file type'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            new_filename = uuid.uuid4().hex + file_ext
            profile.avatar.save(new_filename, avatar_file, save=True)

            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error uploading avatar: {e}")
            return Response(
                {'error': 'Internal server error.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )