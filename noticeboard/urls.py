# from django.urls import path, include
# from .views import BoardViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'board', BoardViewSet)
# urlpatterns = [
#     path('', include(router.urls))
# ]


from django.urls import path
from .views import BoardListAPIView,BoardCreateAPIView, BoardRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('board/list/', BoardListAPIView.as_view(), name='board-list-create'),
    path('board/create/', BoardCreateAPIView.as_view(), name='board-create'),
    path('board/list/<int:pk>/', BoardRetrieveUpdateDestroyAPIView.as_view(), name='board-retrieve-update-destroy'),
]
