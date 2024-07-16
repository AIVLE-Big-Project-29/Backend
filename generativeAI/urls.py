# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('image_generate/', ImageGenerateView.as_view(), name='image_generate'),
]