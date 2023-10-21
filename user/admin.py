from django.contrib import admin
from .models import User 


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','is_active', 'is_staff', 'is_superuser')
    search_fields = ('name', 'email')  
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('name','email')