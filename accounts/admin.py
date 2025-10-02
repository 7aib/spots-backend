from django.contrib import admin

from .models import UserProfile

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_public",
        "age_group",
        "created_at",
    )
    list_filter = ("is_public", "age_group", "is_active", "is_staff", "created_at")
    search_fields = ("username", "email", "first_name", "last_name", "bio")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("username", "email", "first_name", "last_name")},
        ),
        (
            "Profile Information",
            {"fields": ("profile_picture", "bio", "age_group", "is_public")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
