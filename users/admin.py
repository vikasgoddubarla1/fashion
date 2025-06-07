from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email')
    list_display_links = ('id', 'firstname', 'lastname', 'email')
    
admin.site.register(User, UserAdmin)