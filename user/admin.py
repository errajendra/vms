from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'last_login')
    list_filter = ('is_active', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name',)
