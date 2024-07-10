# views.py
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from rest_framework import status

from rest_framework.decorators import api_view, permission_classes

from django.core.mail import send_mail
from django.conf import settings

from django.http import HttpResponseRedirect

import logging

logger = logging.getLogger(__name__)

# 이메일 인증
class EmailVerificationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)
        
        # 기존 인증 기록이 존재하면 삭제
        if EmailVerification.objects.filter(email=email).exists():
            email_verification = EmailVerification.objects.get(email=email)
            
            # 이 토큰을 발행해서 인증을 하지 않았거나 인증을 했으나 계정을 만들지 않았을 경우 삭제
            if not email_verification.is_verified or not User.objects.filter(email=email).exists():
                email_verification.delete()
            else:
                return Response({"error": "Email already verified"}, status=400)

        # 새로운 인증 기록 생성
        email_verification = EmailVerification.objects.create(email=email)
        verification_url = f"{settings.FRONTEND_URL}/user_api/verify-email/{email_verification.token}/"
        # verification_url = f"http://192.168.10.59:8000/user_api/verify-email/{email_verification.token}/"
        send_mail(
            'Email Verification',
            f'Please verify your email by clicking the following link: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({"message": "Verification email sent"}, status=200)

# 이메일 검증
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    try:
        email_verification = EmailVerification.objects.get(token=token)
    except EmailVerification.DoesNotExist:
        return Response({"error": "Invalid token"}, status=400)

    email_verification.deactivate_if_expired()  # 만료 여부를 확인하고 비활성화

    if not email_verification.is_active:
        return Response({"error": "Verification link has expired"}, status=400)

    email_verification.is_verified = True
    email_verification.save()

    # redirect_url = 'http://your-frontend-url.com/email-verified-success'
    # return HttpResponseRedirect(redirect_url)
    return Response({"message": "Email verified successfully"}, status=200)

# 비밀번호 재설정 요청
class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=400)
        
        if not User.objects.filter(email=email).exists():
            return Response({"error": "Email does not exist"}, status=400)

        # 기존 비밀번호 재설정 요청이 존재하면 비활성화
        PasswordResetRequest.objects.filter(email=email, is_active=True).update(is_active=False)

        # 새로운 비밀번호 재설정 요청 생성
        password_reset_request = PasswordResetRequest.objects.create(email=email)
        reset_url = f"{settings.FRONTEND_URL}/user_api/reset-password/{password_reset_request.token}/"
        send_mail(
            'Password Reset Request',
            f'Please reset your password by clicking the following link: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset email sent"}, status=200)

# 비밀번호 재설정
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, token):
    try:
        password_reset_request = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        return Response({"error": "Invalid token"}, status=400)

    password_reset_request.deactivate_if_expired()

    if not password_reset_request.is_active:
        return Response({"error": "Reset link has expired"}, status=400)

    new_password = request.data.get('new_password')
    if not new_password:
        return Response({"error": "New password is required"}, status=400)

    user = User.objects.get(email=password_reset_request.email)
    user.set_password(new_password)
    user.save()

    password_reset_request.is_active = False
    password_reset_request.save()

    return Response({"message": "Password reset successfully"}, status=200)

# 계정생성
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return Response({"error": "GET method is not allowed on this endpoint. Please use POST."}, status=405)

# 계정삭제
class DeleteUserView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user  # 현재 로그인한 사용자
    
    def perform_destroy(self, instance):
        try:
            # 사용자 이메일에 해당하는 EmailVerification 객체 삭제
            EmailVerification.objects.filter(email=instance.email).delete()
            # 사용자 삭제
            instance.delete()
            logger.info(f"User {instance.username} deleted successfully.")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting user {instance.email}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        response = self.perform_destroy(instance)
        return response

# 현재 유저 정보
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user  # 현재 로그인된 사용자 정보
    user_data = {
        'username': user.username,
        'email': user.email,
    }
    return Response(user_data)

# 현재 유저 정보 수정 <- 생각해보니 이게 필요한가?
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def user_info_modify(request):
#     user = request.user
    



# 로그인 인증 테스트용
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_function_view(request):
    print("accept")
    return Response({'message': 'This is a protected function view test'})



# from django.core.mail.message import EmailMessage

# def send_email(request):
#     subject = "message"
#     to = ["pinch4321@gmail.com"]
#     from_email = "test@server.com"
#     message = "메지시 테스트"
#     EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()