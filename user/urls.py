# urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'user_api'

urlpatterns = [
    # 회원가입
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email_request'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),

    # 비밀번호 찾기 테스트 X
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password/<uuid:token>/', reset_password, name='reset_password'),

    # 회원삭제
    path('delete-account/', DeleteUserView.as_view(), name='delete-account'),

    # 로그인 세션 관리
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 테스트
    path('test/', protected_function_view, name="test"),
    path('user_info/', user_info, name='user_info'),
    # path('send_email/', send_email, name='send_email'),
]

# Write by KHJ