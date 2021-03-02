from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Comment, Post, Tag


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ['body']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)
