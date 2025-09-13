# Spots Backend 🏖️

A comprehensive Django REST API backend for a social media platform focused on sharing photos and videos of interesting places and locations. Users can discover, share, and interact with content from various spots around Pakistan.

## 🌟 Features

### 📱 Core Functionality
- **User Authentication**: Token-based authentication system
- **Media Upload**: Upload photos and videos with location tagging
- **Social Feed**: Public feed showing media from all users
- **User Profiles**: Comprehensive user profiles with media galleries
- **Location System**: Places and cities across Pakistan
- **Activity Feed**: Real-time activity tracking (follows, likes, comments)

### 🎯 Social Features
- **Follow System**: Follow/unfollow other users
- **Like & Comment**: Interact with media content
- **Share System**: Share content across platforms
- **Activity Notifications**: Get notified about social interactions
- **Privacy Controls**: Public/private media settings

### 📍 Location Features
- **Places Database**: Curated list of interesting locations
- **City & Province Support**: All major Pakistani cities and provinces
- **Location Tagging**: Tag media with specific places
- **Geographic Filtering**: Filter content by location

## 🏗️ Project Structure

```
spots-backend/
├── accounts/                 # User authentication & management
│   ├── models.py            # User models
│   ├── serializers.py       # Auth serializers
│   ├── views.py             # Login, register, password reset
│   └── urls.py              # Auth endpoints
├── feed/                    # Main content app (renamed from places)
│   ├── models.py            # Media, Places, UserProfile models
│   ├── serializers.py       # Media & feed serializers
│   ├── views.py             # Upload, feed, profile views
│   ├── choices.py           # Age groups, provinces
│   ├── enums.py             # Media types
│   └── urls.py              # Feed endpoints
├── social/                  # Social interactions
│   ├── models.py            # Like, Comment, Share, Follow, Activity
│   ├── serializers.py       # Social serializers
│   ├── views.py             # Social interaction views
│   ├── signals.py           # Activity creation signals
│   ├── enums.py             # Activity types, share platforms
│   └── urls.py              # Social endpoints
├── core/                    # Django project settings
│   ├── settings.py          # Main settings
│   ├── urls.py              # Root URL configuration
│   ├── mixins.py            # Reusable model mixins
│   └── wsgi.py              # WSGI configuration
├── media/                   # User uploaded files
│   ├── media/               # Photos and videos
│   ├── thumbnails/          # Video thumbnails
│   └── profiles/            # Profile pictures
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd spots-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

### Authentication Endpoints
```
POST   /api/auth/register/           # User registration
POST   /api/auth/login/              # User login
POST   /api/auth/logout/             # User logout
POST   /api/auth/password-reset/     # Password reset request
POST   /api/auth/password-reset-confirm/  # Password reset confirmation
```

### Media & Feed Endpoints
```
POST   /api/feed/upload/             # Upload photos/videos
GET    /api/feed/media/              # Public media feed
GET    /api/feed/media/my/           # User's own media
GET    /api/feed/media/{id}/         # Media details
PATCH  /api/feed/media/{id}/update/  # Update media
DELETE /api/feed/media/{id}/delete/  # Delete media
GET    /api/feed/places/             # Available places
```

### User Profile Endpoints
```
GET    /api/feed/profile/{username}/     # User profile by username
GET    /api/feed/profile/id/{user_id}/   # User profile by ID
```

### Social Interaction Endpoints
```
POST   /api/social/follow/{user_id}/     # Follow user
POST   /api/social/unfollow/{user_id}/   # Unfollow user
GET    /api/social/following/            # Following list
GET    /api/social/followers/            # Followers list
POST   /api/social/like/                 # Like content
POST   /api/social/comment/              # Comment on content
```

### Activity Feed Endpoints
```
GET    /api/social/activities/           # User activity feed
GET    /api/social/activities/stats/     # Activity statistics
POST   /api/social/activities/mark-read/ # Mark activities as read
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (for password reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Frontend URL (for password reset links)
FRONTEND_URL=http://localhost:3000
```

### File Upload Settings
- **Max file size**: 100MB
- **Supported photo formats**: JPG, JPEG, PNG, GIF, WebP
- **Supported video formats**: MP4, AVI, MOV, WMV, FLV, WebM
- **Storage**: Local file system (configurable for cloud storage)

## 📊 Database Models

### Core Models
- **User**: Django's built-in user model
- **UserProfile**: Extended user information (bio, age group, city)
- **Media**: Photos and videos with metadata
- **Place**: Location information with coordinates
- **City**: Pakistani cities with province information

### Social Models
- **Follow**: User following relationships
- **Like**: Generic likes on any content
- **Comment**: Comments with nested replies support
- **Share**: Content sharing with platform tracking
- **Activity**: Activity feed for user interactions

## 🎨 Key Features Explained

### Media Upload System
- **Unified Model**: Single model handles both photos and videos
- **File Validation**: Automatic file type and size validation
- **Privacy Controls**: Public/private media settings
- **Location Tagging**: Associate media with specific places
- **Thumbnail Generation**: Auto-generated thumbnails for videos

### Activity Feed
- **Real-time Tracking**: Automatic activity creation for all interactions
- **Rich Notifications**: Detailed activity messages with user info
- **Read Status**: Track which activities have been seen
- **Filtering**: Filter activities by type and read status

### Social System
- **Generic Relations**: Like, comment, and share any content type
- **Nested Comments**: Reply to comments with threading
- **Edit Tracking**: Track when comments are edited
- **Platform Sharing**: Track which platforms content is shared on

## 🔒 Security Features

- **Token Authentication**: Secure API access
- **File Validation**: Prevent malicious file uploads
- **Permission System**: Users can only modify their own content
- **Soft Deletes**: Content is soft-deleted for data recovery
- **Input Validation**: Comprehensive request validation

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run specific app tests:
```bash
python manage.py test feed
python manage.py test social
python manage.py test accounts
```

## 📈 Performance Optimizations

- **Database Indexes**: Optimized queries for feeds and profiles
- **Select Related**: Efficient database queries with joins
- **Pagination**: Large result sets are paginated
- **File Compression**: Optimized media storage
- **Caching Ready**: Structure supports Redis/Memcached

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False`
2. Configure proper `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure static file serving
5. Set up media file storage (AWS S3 recommended)
6. Configure email backend for production

### Docker Support (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Backend Development**: Django REST Framework
- **Database Design**: PostgreSQL/SQLite
- **API Documentation**: Comprehensive endpoint documentation
- **Testing**: Django test framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the code comments for implementation details

## 🔄 Recent Updates

- ✅ Renamed `places` app to `feed` for better clarity
- ✅ Added comprehensive media upload system
- ✅ Implemented activity feed with real-time tracking
- ✅ Created social interaction system (follow, like, comment, share)
- ✅ Added location-based content organization
- ✅ Implemented privacy controls for media
- ✅ Added file validation and security measures

---

**Built with ❤️ using Django REST Framework**
