# Media Upload & Feed API Documentation

This document describes the media upload and feed system for the Spots backend. Users can upload photos and videos that are visible in their profile and shown to other users via the feed.

## Overview

The media system consists of:
- **Media Upload**: Users can upload photos and videos
- **Media Feed**: Public feed showing all users' media
- **User Profile**: Shows user's own media
- **Media Management**: Update, delete, and manage media
- **Social Interactions**: Like, comment, and share media

## Authentication

All upload and management endpoints require authentication using Django REST Framework Token Authentication. Include the token in the Authorization header:

```
Authorization: Token your_token_here
```

## API Endpoints

### Media Upload

#### Upload Media (Photo/Video)
```
POST /api/feed/upload/
```

Upload a new photo or video.

**Request Body (multipart/form-data):**
- `file` (required): The media file to upload
- `media_type` (required): Either "photo" or "video"
- `title` (optional): Title for the media
- `description` (optional): Description for the media
- `place` (optional): ID of the place where media was taken
- `is_public` (optional): Whether media is visible to others (default: true)

**File Validation:**
- **Photos**: JPG, JPEG, PNG, GIF, WebP
- **Videos**: MP4, AVI, MOV, WMV, FLV, WebM
- **Max Size**: 100MB

**Response:**
```json
{
  "message": "Photo uploaded successfully",
  "media": {
    "id": 1,
    "title": "Beautiful sunset",
    "description": "Amazing sunset at the beach",
    "url": "http://localhost:8000/media/media/sunset.jpg",
    "thumbnail_url": null,
    "media_type": "photo",
    "uploaded_by": {
      "id": 1,
      "username": "john_doe",
      "first_name": "John",
      "last_name": "Doe",
      "profile_picture_url": "http://localhost:8000/media/profiles/profile.jpg"
    },
    "place_name": "Beach Resort",
    "place_city": "Karachi",
    "like_count": 0,
    "comment_count": 0,
    "share_count": 0,
    "file_size_mb": 2.5,
    "time_ago": "Just now",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### Media Feed

#### Get Public Media Feed
```
GET /api/feed/media/
```

Get a paginated list of public media from all users.

**Query Parameters:**
- `type` (optional): Filter by media type ("photo" or "video")
- `user_id` (optional): Filter by specific user ID
- `page` (optional): Page number for pagination

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/feed/media/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Beautiful sunset",
      "description": "Amazing sunset at the beach",
      "url": "http://localhost:8000/media/media/sunset.jpg",
      "thumbnail_url": null,
      "media_type": "photo",
      "uploaded_by": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture_url": "http://localhost:8000/media/profiles/profile.jpg"
      },
      "place_name": "Beach Resort",
      "place_city": "Karachi",
      "like_count": 15,
      "comment_count": 3,
      "share_count": 1,
      "file_size_mb": 2.5,
      "time_ago": "2 hours ago",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Get User's Own Media
```
GET /api/feed/media/my/
```

Get the current user's uploaded media (for profile page).

**Response:**
```json
[
  {
    "id": 1,
    "title": "Beautiful sunset",
    "description": "Amazing sunset at the beach",
    "url": "http://localhost:8000/media/media/sunset.jpg",
    "thumbnail_url": null,
    "media_type": "photo",
    "place_name": "Beach Resort",
    "place_city": "Karachi",
    "is_public": true,
    "like_count": 15,
    "comment_count": 3,
    "share_count": 1,
    "file_size_mb": 2.5,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Get Media Details
```
GET /api/feed/media/{media_id}/
```

Get detailed information about a specific media item.

**Response:**
```json
{
  "id": 1,
  "title": "Beautiful sunset",
  "description": "Amazing sunset at the beach",
  "url": "http://localhost:8000/media/media/sunset.jpg",
  "thumbnail_url": null,
  "media_type": "photo",
  "uploaded_by": {
    "id": 1,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "profile_picture_url": "http://localhost:8000/media/profiles/profile.jpg"
  },
  "place_name": "Beach Resort",
  "place_city": "Karachi",
  "like_count": 15,
  "comment_count": 3,
  "share_count": 1,
  "file_size_mb": 2.5,
  "time_ago": "2 hours ago",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Media Management

#### Update Media
```
PATCH /api/feed/media/{media_id}/update/
```

Update media details (title, description, privacy settings).

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "is_public": false
}
```

**Response:**
```json
{
  "message": "Media updated successfully",
  "media": {
    "id": 1,
    "title": "Updated title",
    "description": "Updated description",
    "url": "http://localhost:8000/media/media/sunset.jpg",
    "media_type": "photo",
    "is_public": false,
    "like_count": 15,
    "comment_count": 3,
    "share_count": 1,
    "file_size_mb": 2.5,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Delete Media
```
DELETE /api/feed/media/{media_id}/delete/
```

Delete media (soft delete - can be restored).

**Response:**
```json
{
  "message": "Media deleted successfully"
}
```

### Places

#### Get Places List
```
GET /api/feed/places/
```

Get list of places for media upload.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Beach Resort",
    "description": "Beautiful beach resort",
    "city_name": "Karachi",
    "latitude": "24.8607",
    "longitude": "67.0011"
  }
]
```

## User Profile Integration

The user profile now includes uploaded media:

```
GET /api/feed/profile/{username}/
```

**Response includes:**
```json
{
  "username": "john_doe",
  "uploaded_media": [
    {
      "id": 1,
      "title": "Beautiful sunset",
      "url": "http://localhost:8000/media/media/sunset.jpg",
      "media_type": "photo",
      "like_count": 15,
      "comment_count": 3,
      "share_count": 1,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_videos": 5,
  "total_likes_received": 45,
  "total_comments_received": 12,
  "total_shares_received": 3
}
```

## Social Interactions

Media can be liked, commented on, and shared using the social API:

### Like Media
```
POST /api/social/like/
```

**Request Body:**
```json
{
  "content_type_id": 1,  // ContentType ID for Media
  "object_id": 1         // Media ID
}
```

### Comment on Media
```
POST /api/social/comment/
```

**Request Body:**
```json
{
  "content_type_id": 1,  // ContentType ID for Media
  "object_id": 1,        // Media ID
  "text": "Great photo!"
}
```

### Share Media
```
POST /api/social/share/
```

**Request Body:**
```json
{
  "content_type_id": 1,  // ContentType ID for Media
  "object_id": 1,        // Media ID
  "platform": "facebook",
  "message": "Check out this amazing photo!"
}
```

## File Storage

- **Photos**: Stored in `media/media/` directory
- **Videos**: Stored in `media/media/` directory
- **Thumbnails**: Stored in `media/thumbnails/` directory (auto-generated for videos)
- **Profile Pictures**: Stored in `media/profiles/` directory

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

```json
{
  "error": "Error message description"
}
```

Common error codes:
- `400 Bad Request`: Invalid request data or file format
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Media not found
- `413 Payload Too Large`: File size exceeds limit
- `500 Internal Server Error`: Server error

## Usage Examples

### Frontend Integration

```javascript
// Upload a photo
const uploadPhoto = async (file, title, description, token) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('media_type', 'photo');
  formData.append('title', title);
  formData.append('description', description);
  
  const response = await fetch('/api/feed/upload/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`
    },
    body: formData
  });
  return response.json();
};

// Get media feed
const getMediaFeed = async (type = null) => {
  const url = type ? `/api/feed/media/?type=${type}` : '/api/feed/media/';
  const response = await fetch(url);
  return response.json();
};

// Get user's media
const getUserMedia = async (token) => {
  const response = await fetch('/api/feed/media/my/', {
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  return response.json();
};

// Update media
const updateMedia = async (mediaId, updates, token) => {
  const response = await fetch(`/api/feed/media/${mediaId}/update/`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
  return response.json();
};
```

## Database Migrations

After implementing this system, run the following commands to create the database tables:

```bash
python manage.py makemigrations feed
python manage.py migrate
```

## Admin Interface

The media system includes Django admin interfaces for:
- Media (photos and videos)
- Places
- User Profiles

Access the admin interface at `/admin/` to manage these models.
