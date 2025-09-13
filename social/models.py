from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.mixins import TimeStampedMixin, SoftDeleteMixin, GenericRelationBaseMixin
from social.enums import ActivityType, SharePlatform

class Like(GenericRelationBaseMixin, TimeStampedMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user', 'content_type']),  # For user's likes on specific content types
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.content_object}"
    
    @classmethod
    def get_likes_for_content(cls, content_object):
        """Helper method to get all likes for a specific content object"""
        return cls.objects.filter(
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.pk
        )

class Comment(GenericRelationBaseMixin, TimeStampedMixin, SoftDeleteMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_given')
    text = models.TextField(max_length=500)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return f"{self.user.username} commented on {self.content_object}"
    
    def save(self, *args, **kwargs):
        if self.pk:  # If updating existing comment
            self.is_edited = True
            self.edited_at = timezone.now()
        super().save(*args, **kwargs)
    
    @classmethod
    def get_comments_for_content(cls, content_object):
        """Helper method to get all comments for a specific content object"""
        return cls.objects.filter(
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.pk,
            is_deleted=False
        )

class Share(GenericRelationBaseMixin, TimeStampedMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares_given')
    platform = models.CharField(max_length=20, choices=SharePlatform.choices, default=SharePlatform.OTHER)
    message = models.TextField(max_length=200, blank=True, help_text="Optional message with the share")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['platform']),
        ]

    def __str__(self):
        return f"{self.user.username} shared {self.content_object} on {self.get_platform_display()}"
    
    @classmethod
    def get_shares_for_content(cls, content_object):
        """Helper method to get all shares for a specific content object"""
        return cls.objects.filter(
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.pk
        )

class Follow(TimeStampedMixin, models.Model):
    """Model to track user following relationships"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Activity(TimeStampedMixin, SoftDeleteMixin, models.Model):
    """Model to track all user activities for activity feed"""
    
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities_performed')
    
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities_received')
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)

    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    extra_data = models.JSONField(default=dict, blank=True)
    
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_user', '-created_at']),
            models.Index(fields=['target_user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.actor.username} {self.get_activity_type_display()} - {self.target_user.username}"

    @classmethod
    def create_activity(cls, actor, target_user, activity_type, content_object=None, extra_data=None):
        """Helper method to create activities"""
        return cls.objects.create(
            actor=actor,
            target_user=target_user,
            activity_type=activity_type,
            content_object=content_object,
            extra_data=extra_data or {}
        )