from django.shortcuts import render
from rest_framework import viewsets,status
from .models import User
from .serializers import AddStaffSerializer, ChangePasswordSerializer, SendMailToRecoverSerializer, CheckRecoverTokenSerializer, OldUserToNewSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import secrets
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsSuperUser



class AddStaffUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AddStaffSerializer
    permission_classes = [IsSuperUser, ]

    def create(self, request):
        serializer = AddStaffSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = User.objects.create(name=name, email=email, password=password)
            user.is_staff = True
            user.password = make_password(user.password)
            user.save()

            subject = 'Администратор создал ваш аккаунт'
            message = f"Ваш аккаунт с именем пользователя: {name} и паролем: {password} был создан."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            old_password = serializer.validated_data['old_password']
            user = request.user

            if check_password(old_password, user.password):
                user.password = make_password(new_password)
                user.save()
            else:
                return Response({"message": "неправильный пароль"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "пароль успешно изменен"}, status=status.HTTP_200_OK)
        

class SendTokenToRecoverView(APIView):
    def post(self, request):
        permission_classes = []
        serializer = SendMailToRecoverSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email = email)
            except User.DoesNotExist:
                return Response({"message": "Пользователь с указанным email не существует"})
            
            code = ''.join(secrets.choice('0123456789') for _ in range(6))
            user.email_token = code
            user.save()
            
            subject = 'Восстановить доступ к аккаунту'
            message = f"Чтобы восстановить досутп, введите этот токен на сайте: {code}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "на вашу почту пришел код"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CheckRecoverTokenView(APIView):
    def post(self, request):
        permission_classes = []
        serializer = CheckRecoverTokenSerializer(data = request.data)
        if serializer.is_valid():
            ver_code = serializer.validated_data['token']
            try:
                user = User.objects.filter(email_token = ver_code).first()
                user.email_token = ''
            except User.DoesNotExist:
                return Response({"message": "неправильный токен"})
            
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OldUserToNew(APIView):
    def post(self, request):
        permission_classes = []
        serializer = OldUserToNewSerializer(data = request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']
            user = User.objects.get(name = name)
            refresh = RefreshToken.for_user(user)
            data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            
            }
            if password == confirm_password:
                user.password = make_password(password)
                user.save()
                return Response(data=data, status=200)
            else:
                return Response({"message": "неправильный пароль"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)