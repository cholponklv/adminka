from rest_framework import serializers
from .models import User

class AddStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'email', 'photo', 'is_active', 'is_staff', 'is_superuser')



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length = 255)

    

class SendMailToRecoverSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)



class CheckRecoverTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, min_length=6)


class OldUserToNewSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 255)
    password = serializers.CharField(max_length = 255)
    confirm_password = serializers.CharField(max_length = 255)