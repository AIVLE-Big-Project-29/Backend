from .models import Board
from .serializers import BoardSerializer
from rest_framework import viewsets
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)
