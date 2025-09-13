from rest_framework import serializers
from .models import Video, UserProfile, City
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
    uploaded_media = UserMediaSerializer(source="user.uploaded_videos", many=True, read_only=True)
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
        return obj.user.uploaded_videos.filter(is_deleted=False).count()

    def get_total_likes_received(self, obj):
        """Calculate total likes received on all user's videos"""
        total_likes = 0
        for video in obj.user.uploaded_videos.filter(is_deleted=False):
            total_likes += video.like_count
        return total_likes

    def get_total_comments_received(self, obj):
        """Calculate total comments received on all user's videos"""
        total_comments = 0
        for video in obj.user.uploaded_videos.filter(is_deleted=False):
            total_comments += video.comment_count
        return total_comments

    def get_total_shares_received(self, obj):
        """Calculate total shares received on all user's videos"""
        total_shares = 0
        for video in obj.user.uploaded_videos.filter(is_deleted=False):
            total_shares += video.share_count
        return total_shares
