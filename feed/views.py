from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Video, UserProfile, Media, Place
from .serializers import (
    VideoFeedSerializer, UserProfileSerializer, MediaUploadSerializer, 
    MediaFeedSerializer, UserMediaSerializer, PlaceSerializer
)

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


# -----------------------------
# 📸 Media Upload & Feed Views
# -----------------------------

class MediaUploadView(APIView):
    """View for uploading photos and videos"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """Upload new media (photo or video)"""
        serializer = MediaUploadSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            media = serializer.save()
            
            # Create activity for the upload
            from social.models import Activity
            from social.enums import ActivityType
            
            Activity.create_activity(
                actor=request.user,
                target_user=request.user,  # User sees their own upload
                activity_type=ActivityType.VIDEO_UPLOAD if media.media_type == 'video' else ActivityType.VIDEO_UPLOAD,  # Using same type for now
                content_object=media
            )
            
            response_serializer = MediaFeedSerializer(media, context={'request': request})
            return Response({
                'message': f'{media.get_media_type_display()} uploaded successfully',
                'media': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaFeedView(generics.ListAPIView):
    """View to get public media feed for all users"""
    serializer_class = MediaFeedSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Get public media ordered by latest first"""
        queryset = Media.objects.filter(
            is_public=True,
            is_deleted=False
        ).select_related('uploaded_by', 'place', 'place__city').order_by('-created_at')
        
        # Filter by media type if provided
        media_type = self.request.query_params.get('type')
        if media_type in ['photo', 'video']:
            queryset = queryset.filter(media_type=media_type)
        
        # Filter by user if provided
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(uploaded_by_id=user_id)
        
        return queryset


class UserMediaView(generics.ListAPIView):
    """View to get user's own media (for profile)"""
    serializer_class = UserMediaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get current user's media"""
        return Media.objects.filter(
            uploaded_by=self.request.user,
            is_deleted=False
        ).select_related('place', 'place__city').order_by('-created_at')


class MediaDetailView(generics.RetrieveAPIView):
    """View to get detailed information about a specific media"""
    serializer_class = MediaFeedSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Get media that is public or belongs to the current user"""
        if self.request.user.is_authenticated:
            return Media.objects.filter(
                Q(is_public=True) | Q(uploaded_by=self.request.user),
                is_deleted=False
            ).select_related('uploaded_by', 'place', 'place__city')
        else:
            return Media.objects.filter(
                is_public=True,
                is_deleted=False
            ).select_related('uploaded_by', 'place', 'place__city')


class MediaUpdateView(generics.UpdateAPIView):
    """View to update media details (title, description, privacy)"""
    serializer_class = MediaUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Only allow users to update their own media"""
        return Media.objects.filter(
            uploaded_by=self.request.user,
            is_deleted=False
        )
    
    def update(self, request, *args, **kwargs):
        """Update media with partial data"""
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            response_serializer = MediaFeedSerializer(instance, context={'request': request})
            return Response({
                'message': 'Media updated successfully',
                'media': response_serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaDeleteView(generics.DestroyAPIView):
    """View to delete media (soft delete)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Only allow users to delete their own media"""
        return Media.objects.filter(
            uploaded_by=self.request.user,
            is_deleted=False
        )
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete the media"""
        instance = self.get_object()
        instance.delete()  # This will soft delete due to SoftDeleteMixin
        return Response({'message': 'Media deleted successfully'}, status=status.HTTP_200_OK)


class PlacesListView(generics.ListAPIView):
    """View to get list of places for media upload"""
    serializer_class = PlaceSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Get all places ordered by name"""
        return Place.objects.filter(is_deleted=False).select_related('city').order_by('name')

