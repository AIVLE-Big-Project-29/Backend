from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'affiliation', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'affiliation')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_image', 'affiliation')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_image', 'affiliation')}),
    )
