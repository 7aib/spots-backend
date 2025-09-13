from django.urls import path
from .views import VideoFeedView, UserProfileView, UserProfileByIDView

urlpatterns = [
    path("feed/", VideoFeedView.as_view(), name="video-feed"),
    path("profile/<str:username>/", UserProfileView.as_view(), name="user-profile"),
    path("profile/id/<int:user_id>/", UserProfileByIDView.as_view(), name="user-profile-by-id"),
]
