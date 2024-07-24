# from .models import Board
# from .serializers import BoardSerializer
# from rest_framework import viewsets,serializers
# from .permissions import IsAuthorOrReadOnly
# from rest_framework.permissions import AllowAny ,IsAuthenticated

# class BoardViewSet(viewsets.ModelViewSet):
#     queryset = Board.objects.all()
#     serializer_class = BoardSerializer
#     permission_classes = [AllowAny]

#     def perform_create(self, serializer):
#         serializer.save()
        
#     def perform_update(self, serializer):
#         serializer.save()


from .models import Board
from .serializers import BoardSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import AllowAny ,IsAuthenticated


class BoardListAPIView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]


class BoardCreateAPIView(CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]
# user=self.request.user
    def perform_create(self, serializer):
        serializer.save()
    
class BoardRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()