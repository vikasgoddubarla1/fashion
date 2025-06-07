from rest_framework import serializers
from .models import *


class BlogSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category_id.name')
    class Meta:
        model = Blog
        fields = ('id', 'category_id', 'category_name', "status", 'title', 'content', 'meta_title', 'meta_description', 'image', 'focus_keyword', 'other_keywords', 'created_by', 'created_at')


class BlogListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category_id.name')
    
    class Meta:
        model = Blog
        fields = ('id', 'category_id', 'category_name', 'title', 'status')