from rest_framework import serializers
from .models import Video, UserProfile, City, Media, Place
from django.contrib.auth.models import User

class VideoFeedSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    uploaded_by = serializers.StringRelatedField()  # shows username instead of ID
    place_name = serializers.CharField(source="place.name", read_only=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "url",
            "uploaded_by",
            "place_name",
            "created_at",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url)

class UserMediaSerializer(serializers.ModelSerializer):
    """Serializer for user's uploaded media with metadata"""
    url = serializers.SerializerMethodField()
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    share_count = serializers.ReadOnlyField()
    place_name = serializers.CharField(source="place.name", read_only=True)
    place_city = serializers.CharField(source="place.city.name", read_only=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "url",
            "place_name",
            "place_city",
            "like_count",
            "comment_count",
            "share_count",
            "created_at",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url)

class CitySerializer(serializers.ModelSerializer):
    """Serializer for city information"""
    class Meta:
        model = City
        fields = ["id", "name", "province"]

class UserProfileSerializer(serializers.ModelSerializer):
    """Comprehensive user profile serializer"""
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    profile_picture_url = serializers.SerializerMethodField()
    city_info = CitySerializer(source="city", read_only=True)
    uploaded_media = UserMediaSerializer(source="user.uploaded_media", many=True, read_only=True)
    total_videos = serializers.SerializerMethodField()
    total_likes_received = serializers.SerializerMethodField()
    total_comments_received = serializers.SerializerMethodField()
    total_shares_received = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture_url",
            "bio",
            "city_info",
            "age_group",
            "uploaded_media",
            "total_videos",
            "total_likes_received",
            "total_comments_received",
            "total_shares_received",
            "created_at",
        ]

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.profile_picture.url)
        return None

    def get_total_videos(self, obj):
        return obj.user.uploaded_media.filter(is_deleted=False).count()

    def get_total_likes_received(self, obj):
        """Calculate total likes received on all user's media"""
        total_likes = 0
        for media in obj.user.uploaded_media.filter(is_deleted=False):
            total_likes += media.like_count
        return total_likes

    def get_total_comments_received(self, obj):
        """Calculate total comments received on all user's media"""
        total_comments = 0
        for media in obj.user.uploaded_media.filter(is_deleted=False):
            total_comments += media.comment_count
        return total_comments

    def get_total_shares_received(self, obj):
        """Calculate total shares received on all user's media"""
        total_shares = 0
        for media in obj.user.uploaded_media.filter(is_deleted=False):
            total_shares += media.share_count
        return total_shares


# -----------------------------
# 📸 Media Serializers
# -----------------------------

class MediaUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading media (photos/videos)"""
    file_size_mb = serializers.ReadOnlyField()
    
    class Meta:
        model = Media
        fields = [
            'title', 'description', 'file', 'media_type', 
            'place', 'is_public', 'file_size_mb'
        ]
    
    def validate_file(self, value):
        """Validate uploaded file"""
        if not value:
            raise serializers.ValidationError("No file provided")
        
        # Check file size (max 100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 100MB")
        
        # Check file type based on media_type
        media_type = self.initial_data.get('media_type')
        if media_type == 'photo':
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            if not any(value.name.lower().endswith(ext) for ext in allowed_extensions):
                raise serializers.ValidationError("Invalid photo format. Allowed: JPG, PNG, GIF, WebP")
        elif media_type == 'video':
            allowed_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
            if not any(value.name.lower().endswith(ext) for ext in allowed_extensions):
                raise serializers.ValidationError("Invalid video format. Allowed: MP4, AVI, MOV, WMV, FLV, WebM")
        
        return value
    
    def validate_media_type(self, value):
        """Validate media type"""
        if value not in ['photo', 'video']:
            raise serializers.ValidationError("Media type must be either 'photo' or 'video'")
        return value
    
    def create(self, validated_data):
        """Create media instance with uploaded_by user"""
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class MediaFeedSerializer(serializers.ModelSerializer):
    """Serializer for displaying media in feed"""
    url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    uploaded_by = serializers.SerializerMethodField()
    place_name = serializers.CharField(source="place.name", read_only=True)
    place_city = serializers.CharField(source="place.city.name", read_only=True)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    share_count = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Media
        fields = [
            'id', 'title', 'description', 'url', 'thumbnail_url',
            'media_type', 'uploaded_by', 'place_name', 'place_city',
            'like_count', 'comment_count', 'share_count', 
            'file_size_mb', 'time_ago', 'created_at'
        ]
    
    def get_url(self, obj):
        """Get full URL for the media file"""
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url)
    
    def get_thumbnail_url(self, obj):
        """Get thumbnail URL if available"""
        if obj.thumbnail:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.thumbnail.url)
        return None
    
    def get_uploaded_by(self, obj):
        """Get user information who uploaded the media"""
        return {
            'id': obj.uploaded_by.id,
            'username': obj.uploaded_by.username,
            'first_name': obj.uploaded_by.first_name,
            'last_name': obj.uploaded_by.last_name,
            'profile_picture_url': self._get_profile_picture_url(obj.uploaded_by)
        }
    
    def _get_profile_picture_url(self, user):
        """Get user's profile picture URL"""
        try:
            profile = user.profile
            if profile.profile_picture:
                request = self.context.get("request")
                return request.build_absolute_uri(profile.profile_picture.url)
        except UserProfile.DoesNotExist:
            pass
        return None
    
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


class UserMediaSerializer(serializers.ModelSerializer):
    """Serializer for user's own media in profile"""
    url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    share_count = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    place_name = serializers.CharField(source="place.name", read_only=True)
    place_city = serializers.CharField(source="place.city.name", read_only=True)

    class Meta:
        model = Media
        fields = [
            "id", "title", "description", "url", "thumbnail_url",
            "media_type", "place_name", "place_city", "is_public",
            "like_count", "comment_count", "share_count", 
            "file_size_mb", "created_at"
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url)
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.thumbnail.url)
        return None


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for places"""
    city_name = serializers.CharField(source="city.name", read_only=True)
    
    class Meta:
        model = Place
        fields = ['id', 'name', 'description', 'city_name', 'latitude', 'longitude']
