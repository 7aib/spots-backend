# Activity System API Documentation

This document describes the activity system API endpoints for the Spots backend. The activity system tracks user interactions like follows, likes, comments, and shares to provide users with a personalized activity feed.

## Overview

The activity system consists of:
- **Activity Feed**: Shows activities related to the logged-in user
- **Follow System**: Users can follow/unfollow other users
- **Social Interactions**: Like, comment, and share content
- **Activity Statistics**: Get counts and statistics about activities

## Authentication

All endpoints require authentication using Django REST Framework Token Authentication. Include the token in the Authorization header:

```
Authorization: Token your_token_here
```

## API Endpoints

### Activity Feed

#### Get Activity Feed
```
GET /api/social/activities/
```

Returns a paginated list of activities for the logged-in user.

**Query Parameters:**
- `type` (optional): Filter by activity type (`follow`, `like`, `comment`, `share`, `video_upload`, `place_created`)
- `is_read` (optional): Filter by read status (`true` or `false`)

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/social/activities/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "actor": {
        "id": 2,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture_url": "http://localhost:8000/media/profiles/profile.jpg"
      },
      "activity_type": "follow",
      "content_object_data": null,
      "activity_message": "John started following you",
      "time_ago": "2 hours ago",
      "is_read": false,
      "created_at": "2024-01-15T10:30:00Z",
      "extra_data": {}
    },
    {
      "id": 2,
      "actor": {
        "id": 3,
        "username": "jane_smith",
        "first_name": "Jane",
        "last_name": "Smith",
        "profile_picture_url": null
      },
      "activity_type": "like",
      "content_object_data": {
        "id": 1,
        "type": "video",
        "title": "Amazing sunset",
        "url": "http://localhost:8000/media/videos/sunset.mp4"
      },
      "activity_message": "Jane liked your video",
      "time_ago": "1 day ago",
      "is_read": true,
      "created_at": "2024-01-14T15:45:00Z",
      "extra_data": {}
    }
  ]
}
```

#### Get Activity Statistics
```
GET /api/social/activities/stats/
```

Returns statistics about the user's activities.

**Response:**
```json
{
  "total_activities": 25,
  "unread_count": 5,
  "activities_by_type": {
    "like": 10,
    "follow": 8,
    "comment": 4,
    "share": 2,
    "video_upload": 1
  }
}
```

#### Mark Activities as Read
```
POST /api/social/activities/mark-read/
```

Mark activities as read for the current user.

**Request Body:**
```json
{
  "activity_ids": [1, 2, 3]  // Optional: specific activity IDs to mark as read
}
```

If `activity_ids` is not provided, all activities will be marked as read.

**Response:**
```json
{
  "message": "Activities marked as read"
}
```

### Follow System

#### Follow a User
```
POST /api/social/follow/{user_id}/
```

Follow another user.

**Response:**
```json
{
  "message": "User followed successfully"
}
```

#### Unfollow a User
```
POST /api/social/unfollow/{user_id}/
```

Unfollow a user.

**Response:**
```json
{
  "message": "User unfollowed successfully"
}
```

#### Get Following List
```
GET /api/social/following/
```

Get list of users that the current user is following.

**Response:**
```json
[
  {
    "id": 1,
    "follower": {
      "id": 1,
      "username": "current_user",
      "first_name": "Current",
      "last_name": "User",
      "profile_picture_url": null
    },
    "following": {
      "id": 2,
      "username": "john_doe",
      "first_name": "John",
      "last_name": "Doe",
      "profile_picture_url": "http://localhost:8000/media/profiles/profile.jpg"
    },
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Get Followers List
```
GET /api/social/followers/
```

Get list of users that follow the current user.

**Response:**
```json
[
  {
    "id": 1,
    "follower": {
      "id": 2,
      "username": "john_doe",
      "first_name": "John",
      "last_name": "Doe",
      "profile_picture_url": "http://localhost:8000/media/profiles/profile.jpg"
    },
    "following": {
      "id": 1,
      "username": "current_user",
      "first_name": "Current",
      "last_name": "User",
      "profile_picture_url": null
    },
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Social Interactions

#### Toggle Like
```
POST /api/social/like/
```

Like or unlike a content object (video, place, etc.).

**Request Body:**
```json
{
  "content_type_id": 1,  // ContentType ID for the object
  "object_id": 5         // ID of the specific object
}
```

**Response:**
```json
{
  "message": "Liked successfully",
  "liked": true
}
```

#### Add Comment
```
POST /api/social/comment/
```

Add a comment to a content object.

**Request Body:**
```json
{
  "content_type_id": 1,  // ContentType ID for the object
  "object_id": 5,        // ID of the specific object
  "text": "Great video!" // Comment text
}
```

**Response:**
```json
{
  "message": "Comment added successfully",
  "comment_id": 10
}
```

## Activity Types

The system tracks the following activity types (defined in `social/enums.py`):

1. **follow**: When someone follows you
2. **like**: When someone likes your content
3. **comment**: When someone comments on your content
4. **share**: When someone shares your content
5. **video_upload**: When you upload a video (for your own feed)
6. **place_created**: When you create a place (for your own feed)

All activity types are now properly defined using Django's `TextChoices` for better type safety and consistency.

## Content Types

The system supports activities on the following content types:
- Videos
- Places
- User Profiles

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

```json
{
  "error": "Error message description"
}
```

Common error codes:
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Usage Examples

### Frontend Integration

```javascript
// Get activity feed
const getActivityFeed = async (token) => {
  const response = await fetch('/api/social/activities/', {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};

// Follow a user
const followUser = async (userId, token) => {
  const response = await fetch(`/api/social/follow/${userId}/`, {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};

// Like a video
const likeVideo = async (videoId, token) => {
  const response = await fetch('/api/social/like/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      content_type_id: 1, // Video content type ID
      object_id: videoId
    })
  });
  return response.json();
};
```

## Database Migrations

After implementing this system, run the following commands to create the database tables:

```bash
python manage.py makemigrations social
python manage.py migrate
```

## Admin Interface

The activity system includes Django admin interfaces for:
- Activities
- Follows
- Likes
- Comments
- Shares

Access the admin interface at `/admin/` to manage these models.
