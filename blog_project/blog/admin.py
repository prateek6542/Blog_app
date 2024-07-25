from django.contrib import admin
from .models import Blog, Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
    list_filter = ('created_at', 'updated_at', 'author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog', 'created_at')
    search_fields = ('body',)
    list_filter = ('created_at', 'author')
