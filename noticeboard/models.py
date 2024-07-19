from django.db import models
from django.conf import settings

class Board(models.Model):
    id = models.AutoField(primary_key=True, null= False, blank =False)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, blank = True, on_delete=models.CASCADE)
    content = models.TextField()
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)
    file = models.FileField(upload_to='files/')
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)