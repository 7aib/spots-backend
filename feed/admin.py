from django.contrib import admin
from .models import UserProfile, City, Category, Place, Video

# 🧍 User Profile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "age_group")
    search_fields = ("user__username", "city__name")
    list_filter = ("age_group", "city")
# 🏙️ City
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "province")
    search_fields = ("name",)

# 🗂️ Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# 📍 Place
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "city", "created_by")
    search_fields = ("name", "description")
    list_filter = ("category", "city")

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = "Likes"

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = "Comments"

    def shares_count(self, obj):
        return obj.shares.count()
    shares_count.short_description = "Shares"

# 📸 Video
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "place", "created_at")
    search_fields = ("title",)
    list_filter = ("place",)
