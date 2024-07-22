from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('created_at', 'updated_at', 'user')
