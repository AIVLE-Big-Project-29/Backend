from .models import Board
from rest_framework import serializers

class BoardSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Board
        fields = ['id','title','user','content','created_at','updated_at',]
