# models.py
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import uuid

from datetime import timedelta
from django.utils import timezone

# 이메일 인증
class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # 새로운 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=3)  # 3분 동안 유효

    def deactivate_if_expired(self):
        if self.is_expired():
            self.is_active = False
            self.save()
    
    def deactivate_if_create(self):
        self.is_active = False
        self.save()

# 비밀번호 재설정 이메일 인증
class PasswordResetRequest(models.Model):
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=3)  # 30분 동안 유효

    def deactivate_if_expired(self):
        if self.is_expired():
            self.is_active = False
            self.save()