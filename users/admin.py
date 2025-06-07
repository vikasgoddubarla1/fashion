from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_display_links = ('id', 'first_name', 'last_name', 'email')
    
admin.site.register(User, UserAdmin)