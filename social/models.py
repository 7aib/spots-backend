from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User
from core.mixins import TimeStampedMixin, SoftDeleteMixin, GenericRelationBaseMixin

class Like(GenericRelationBaseMixin, TimeStampedMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} liked {self.content_object}"

class Comment(GenericRelationBaseMixin, TimeStampedMixin, SoftDeleteMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.content_object}"

class Share(GenericRelationBaseMixin, TimeStampedMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} shared {self.content_object}"
