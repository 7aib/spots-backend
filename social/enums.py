from django.db import models

class ActivityType(models.TextChoices):
    FOLLOW = "follow", "Follow"
    LIKE = "like", "Like"
    COMMENT = "comment", "Comment"
    SHARE = "share", "Share"
    VIDEO_UPLOAD = "video_upload", "Video Upload"
    PLACE_CREATED = "place_created", "Place Created"

class SharePlatform(models.TextChoices):
    FACEBOOK = "facebook", "Facebook"
    TWITTER = "twitter", "Twitter"
    INSTAGRAM = "instagram", "Instagram"
    WHATSAPP = "whatsapp", "WhatsApp"
    TELEGRAM = "telegram", "Telegram"
    COPY_LINK = "copy_link", "Copy Link"
    OTHER = "other", "Other"
