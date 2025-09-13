from django.urls import path
from . import views

urlpatterns = [
    # Activity feed endpoints
    path('activities/', views.ActivityFeedView.as_view(), name='activity-feed'),
    path('activities/stats/', views.ActivityStatsView.as_view(), name='activity-stats'),
    path('activities/mark-read/', views.MarkActivitiesAsReadView.as_view(), name='mark-activities-read'),
    
    # Follow/unfollow endpoints
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
    path('following/', views.FollowingListView.as_view(), name='following-list'),
    path('followers/', views.FollowersListView.as_view(), name='followers-list'),
    
    # Social interactions
    path('like/', views.ToggleLikeView.as_view(), name='toggle-like'),
    path('comment/', views.AddCommentView.as_view(), name='add-comment'),
]
