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
from user.models import CustomUser

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
    def perform_create(self, serializer):
        # user = CustomUser.objects.filter(id=self.request.user)    
        serializer.save(user=self.request.user)
    
class BoardRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()