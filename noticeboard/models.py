from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    id = models.AutoField(primary_key=True, null= False, blank =False)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, null = True, blank = True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    