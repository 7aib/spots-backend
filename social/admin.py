from django.contrib import admin
from .models import Like, Comment, Share, Follow, Activity


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['user__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'text', 'created_at', 'is_deleted']
    list_filter = ['content_type', 'created_at', 'is_deleted']
    search_fields = ['user__username', 'text']


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'platform', 'created_at']
    list_filter = ['content_type', 'platform', 'created_at']
    search_fields = ['user__username']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['actor', 'target_user', 'activity_type', 'is_read', 'created_at']
    list_filter = ['activity_type', 'is_read', 'created_at']
    search_fields = ['actor__username', 'target_user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('actor', 'target_user', 'content_type')
