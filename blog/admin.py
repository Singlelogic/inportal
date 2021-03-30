from django.contrib import admin

from .models import Comment, Post, Tag


admin.site.register(Post)
admin.site.register(Tag)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created',)
    list_filter = ('post', 'user', 'created',)
    search_fields = ('body',)


admin.site.register(Comment, CommentAdmin)
