from django.urls import path
from .views import (
    UserProfileView, UserProfileByIDView,
    MediaUploadView, MediaFeedView, UserMediaView, MediaDetailView,
    MediaUpdateView, MediaDeleteView, PlacesListView
)

urlpatterns = [
    # User profiles
    path("profile/<str:username>/", UserProfileView.as_view(), name="user-profile"),
    path("profile/id/<int:user_id>/", UserProfileByIDView.as_view(), name="user-profile-by-id"),
    
    # Media upload and management
    path("upload/", MediaUploadView.as_view(), name="media-upload"),
    path("media/", MediaFeedView.as_view(), name="media-feed"),
    path("media/my/", UserMediaView.as_view(), name="user-media"),
    path("media/<int:pk>/", MediaDetailView.as_view(), name="media-detail"),
    path("media/<int:pk>/update/", MediaUpdateView.as_view(), name="media-update"),
    path("media/<int:pk>/delete/", MediaDeleteView.as_view(), name="media-delete"),
    
    # Places for media upload
    path("places/", PlacesListView.as_view(), name="places-list"),
]
