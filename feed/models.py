from django.db import models
from django.contrib.auth.models import User
from core.mixins import TimeStampedMixin, SoftDeleteMixin
from django.contrib.contenttypes.fields import GenericRelation
from .choices import Provinces, AgeGroup
from social.models import Like, Comment, Share

# -----------------------------
# 🧍 User Profile
# -----------------------------

class UserProfile(TimeStampedMixin, SoftDeleteMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)
    age_group = models.CharField(
        max_length=10,
        choices=AgeGroup.choices,
        blank=True,
        null=True
    )
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    shares = GenericRelation(Share)


    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def share_count(self):
        return self.shares.count()

    def __str__(self):
        return self.user.username


# -----------------------------
# 🏙️ City
# -----------------------------

class City(TimeStampedMixin, SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.CharField(max_length=100, choices=Provinces, default='punjab')

    def __str__(self):
        return self.name

# -----------------------------
# 🗂️ Category
# -----------------------------

class Category(TimeStampedMixin, SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# -----------------------------
# 📍 Place
# -----------------------------

class Place(TimeStampedMixin, SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    shares = GenericRelation(Share)

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def share_count(self):
        return self.shares.count()

    def __str__(self):
        return self.name

# -----------------------------
# 📸 Videos
# -----------------------------

class Video(TimeStampedMixin, SoftDeleteMixin, models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to="videos/")
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_videos')
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    shares = GenericRelation(Share)

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def share_count(self):
        return self.shares.count()

    def __str__(self):
        return self.title or f"Video {self.id}"
