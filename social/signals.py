from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .models import Activity
from .enums import ActivityType
from feed.models import Video, Place


@receiver(post_save, sender=Video)
def create_video_upload_activity(sender, instance, created, **kwargs):
    """Create activity when a video is uploaded"""
    if created:
        # Create activity for the user who uploaded the video
        # This could be used to show in their own activity feed or for followers
        Activity.create_activity(
            actor=instance.uploaded_by,
            target_user=instance.uploaded_by,  # User sees their own upload
            activity_type=ActivityType.VIDEO_UPLOAD,
            content_object=instance
        )


@receiver(post_save, sender=Place)
def create_place_created_activity(sender, instance, created, **kwargs):
    """Create activity when a place is created"""
    if created:
        # Create activity for the user who created the place
        Activity.create_activity(
            actor=instance.created_by,
            target_user=instance.created_by,  # User sees their own creation
            activity_type=ActivityType.PLACE_CREATED,
            content_object=instance
        )
