from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Video, UserProfile
from .serializers import VideoFeedSerializer, UserProfileSerializer

class VideoFeedView(generics.ListAPIView):
    queryset = Video.objects.all().order_by("-created_at")  # latest first
    serializer_class = VideoFeedSerializer
    permission_classes = [permissions.AllowAny]  # public feed

class UserProfileView(generics.RetrieveAPIView):
    """View to get user profile with all uploaded media and metadata"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]  # public profiles
    
    def get_object(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile

class UserProfileByIDView(generics.RetrieveAPIView):
    """View to get user profile by user ID"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]  # public profiles
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile

