from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from mptt.admin import MPTTModelAdmin
from .models import Board, Topic, Post, Comment, IpModel, TopicRequest



class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('post',)
    inlines = [
        CommentInline,
    ]
    list_display = ('title', 'post', 'writer', 'date_created',)
    search_fields = [
        'writer__username__exact',
        'post__icontains',
        'title__icontains',
    ]

class TopicRequestAdmin(admin.ModelAdmin):
    list_display = ('category', 'topic', 'date_created',)


admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(IpModel)
admin.site.register(TopicRequest, TopicRequestAdmin)