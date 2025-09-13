from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta

from .models import Activity, Follow, Like, Comment, Share
from .serializers import ActivitySerializer, FollowSerializer, ActivityStatsSerializer
from .enums import ActivityType
from feed.models import Place


class ActivityFeedView(generics.ListAPIView):
    """View to get the activity feed for the logged-in user"""
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get activities for the current user"""
        user = self.request.user
        
        # Get activities where the current user is the target
        queryset = Activity.objects.filter(target_user=user).select_related(
            'actor', 'content_type'
        ).prefetch_related('content_object')
        
        # Filter by activity type if provided
        activity_type = self.request.query_params.get('type')
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Filter by read status if provided
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        return queryset


class ActivityStatsView(generics.RetrieveAPIView):
    """View to get activity statistics for the logged-in user"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivityStatsSerializer
    
    def get_object(self):
        """Get activity statistics for the current user"""
        user = self.request.user
        
        # Get total activities
        total_activities = Activity.objects.filter(target_user=user).count()
        
        # Get unread count
        unread_count = Activity.objects.filter(target_user=user, is_read=False).count()
        
        # Get activities by type
        activities_by_type = Activity.objects.filter(target_user=user).values(
            'activity_type'
        ).annotate(count=Count('id')).order_by('-count')
        
        activities_by_type_dict = {item['activity_type']: item['count'] for item in activities_by_type}
        
        return {
            'total_activities': total_activities,
            'unread_count': unread_count,
            'activities_by_type': activities_by_type_dict
        }


class MarkActivitiesAsReadView(APIView):
    """Mark activities as read for the current user"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        activity_ids = request.data.get('activity_ids', [])
        
        if activity_ids:
            # Mark specific activities as read
            Activity.objects.filter(
                id__in=activity_ids,
                target_user=user
            ).update(is_read=True)
        else:
            # Mark all activities as read
            Activity.objects.filter(target_user=user).update(is_read=True)
        
        return Response({'message': 'Activities marked as read'}, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    """Follow a user"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if user_to_follow == request.user:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if created:
            # Create activity for the followed user
            Activity.create_activity(
                actor=request.user,
                target_user=user_to_follow,
                activity_type=ActivityType.FOLLOW
            )
            return Response({'message': 'User followed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already following this user'}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    """Unfollow a user"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            follow = Follow.objects.get(follower=request.user, following=user_to_unfollow)
            follow.delete()
            return Response({'message': 'User unfollowed successfully'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({'error': 'Not following this user'}, status=status.HTTP_400_BAD_REQUEST)


class FollowingListView(generics.ListAPIView):
    """Get list of users that the current user is following"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user).select_related('following')


class FollowersListView(generics.ListAPIView):
    """Get list of users that follow the current user"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user).select_related('follower')


class ToggleLikeView(APIView):
    """Toggle like on a content object"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        content_type_id = request.data.get('content_type_id')
        object_id = request.data.get('object_id')
        
        if not content_type_id or not object_id:
            return Response({'error': 'content_type_id and object_id are required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            content_type = ContentType.objects.get(id=content_type_id)
            content_object = content_type.get_object_for_this_type(id=object_id)
        except (ContentType.DoesNotExist, Exception):
            return Response({'error': 'Content object not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already liked
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        )
        
        if created:
            # Create activity for the content owner
            target_user = None
            if hasattr(content_object, 'uploaded_by'):
                target_user = content_object.uploaded_by
            elif hasattr(content_object, 'created_by'):
                target_user = content_object.created_by
            elif hasattr(content_object, 'user'):
                target_user = content_object.user
            
            if target_user and target_user != request.user:
                Activity.create_activity(
                    actor=request.user,
                    target_user=target_user,
                    activity_type=ActivityType.LIKE,
                    content_object=content_object
                )
            
            return Response({'message': 'Liked successfully', 'liked': True}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({'message': 'Unliked successfully', 'liked': False}, status=status.HTTP_200_OK)


class AddCommentView(APIView):
    """Add a comment to a content object"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        content_type_id = request.data.get('content_type_id')
        object_id = request.data.get('object_id')
        text = request.data.get('text', '').strip()
        
        if not content_type_id or not object_id or not text:
            return Response({'error': 'content_type_id, object_id, and text are required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            content_type = ContentType.objects.get(id=content_type_id)
            content_object = content_type.get_object_for_this_type(id=object_id)
        except (ContentType.DoesNotExist, Exception):
            return Response({'error': 'Content object not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create comment
        comment = Comment.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            text=text
        )
        
        # Create activity for the content owner
        target_user = None
        if hasattr(content_object, 'uploaded_by'):
            target_user = content_object.uploaded_by
        elif hasattr(content_object, 'created_by'):
            target_user = content_object.created_by
        elif hasattr(content_object, 'user'):
            target_user = content_object.user
        
        if target_user and target_user != request.user:
            Activity.create_activity(
                actor=request.user,
                target_user=target_user,
                activity_type=ActivityType.COMMENT,
                content_object=content_object,
                extra_data={'comment_text': text[:100]}  # Store first 100 chars
            )
        
        return Response({'message': 'Comment added successfully', 'comment_id': comment.id}, 
                       status=status.HTTP_201_CREATED)
