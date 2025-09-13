from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import Like, Comment, Share, Follow, Activity
from feed.models import Place, UserProfile


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user information for activity feed"""
    profile_picture_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture_url']
    
    def get_profile_picture_url(self, obj):
        try:
            profile = obj.profile
            if profile.profile_picture:
                request = self.context.get("request")
                return request.build_absolute_uri(profile.profile_picture.url)
        except UserProfile.DoesNotExist:
            pass
        return None


class ContentObjectSerializer(serializers.Serializer):
    """Serializer for content objects in activities"""
    id = serializers.IntegerField()
    type = serializers.CharField()
    title = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    text = serializers.CharField(required=False)
    url = serializers.URLField(required=False)
    
    def to_representation(self, instance):
        if instance is None:
            return None
            
        data = {
            'id': instance.id,
            'type': instance.__class__.__name__.lower()
        }
        
        # Add specific fields based on the object type
        if hasattr(instance, 'title'):
            data['title'] = instance.title
        elif hasattr(instance, 'name'):
            data['name'] = instance.name
        elif hasattr(instance, 'text'):
            data['text'] = instance.text
            
        # Add URL if it's a media object
        if hasattr(instance, 'file') and instance.file:
            request = self.context.get("request")
            data['url'] = request.build_absolute_uri(instance.file.url)
        elif hasattr(instance, 'profile_picture') and instance.profile_picture:
            request = self.context.get("request")
            data['url'] = request.build_absolute_uri(instance.profile_picture.url)
            
        return data


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for user activities"""
    actor = UserBasicSerializer(read_only=True)
    content_object_data = serializers.SerializerMethodField()
    activity_message = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'actor', 'activity_type', 'content_object_data', 
            'activity_message', 'time_ago', 'is_read', 'created_at', 'extra_data'
        ]
    
    def get_content_object_data(self, obj):
        if obj.content_object:
            return ContentObjectSerializer(obj.content_object, context=self.context).data
        return None
    
    def get_activity_message(self, obj):
        """Generate human-readable activity message"""
        actor_name = obj.actor.first_name or obj.actor.username
        
        messages = {
            'follow': f"{actor_name} started following you",
            'like': f"{actor_name} liked your {self._get_content_type_name(obj)}",
            'comment': f"{actor_name} commented on your {self._get_content_type_name(obj)}",
            'share': f"{actor_name} shared your {self._get_content_type_name(obj)}",
            'video_upload': f"{actor_name} uploaded a new video",
            'place_created': f"{actor_name} created a new place",
        }
        
        return messages.get(obj.activity_type, f"{actor_name} performed an action")
    
    def _get_content_type_name(self, obj):
        """Get a human-readable name for the content type"""
        if not obj.content_object:
            return "content"
            
        content_type_map = {
            'video': 'video',
            'place': 'place',
            'userprofile': 'profile',
        }
        
        return content_type_map.get(
            obj.content_object.__class__.__name__.lower(), 
            'content'
        )
    
    def get_time_ago(self, obj):
        """Get human-readable time difference"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for follow relationships"""
    follower = UserBasicSerializer(read_only=True)
    following = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']


class ActivityStatsSerializer(serializers.Serializer):
    """Serializer for activity statistics"""
    total_activities = serializers.IntegerField()
    unread_count = serializers.IntegerField()
    activities_by_type = serializers.DictField()
