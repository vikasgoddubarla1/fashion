from django.db import models
from users.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=155, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Blog(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    image   = models.ImageField(upload_to="blog/images", null=True, blank=True)
    meta_title = models.CharField(max_length=60)
    meta_description = models.CharField(max_length=160)
    focus_keyword = models.CharField(max_length=50)
    other_keywords = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = (
        ('published', 'published'),
        ('draft', 'draft'),
        ('scheduled', 'scheduled'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    