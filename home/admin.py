from django.contrib import admin
from .models import Post, Comment, Vote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated', 'created')
    search_fields = ('slug',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_reply', 'created')
    search_fields = ('body',)
    raw_id_fields = ('user', 'post', 'reply')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    raw_id_fields = ('post',)
