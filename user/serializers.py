# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmailVerification

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        try:
            email_verification = EmailVerification.objects.get(email=email)
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Email is not verified")

        email_verification.deactivate_if_expired()  # 만료 여부를 확인하고 비활성화

        if not email_verification.is_verified or not email_verification.is_active: # 이미 인증되어 있거나 기간이 만료되었으면
            raise serializers.ValidationError("Email is not verified or the verification link has expired")

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        email_verification.deactivate_if_create() # 생성했으니 비활성화
        # email_verification.delete()  # 인증 정보를 사용 후 삭제

        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')