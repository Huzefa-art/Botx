from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserModelAdmin(UserAdmin):
    
    list_display = ["id", "username", "email", "is_superuser"]
    list_filter = ["is_superuser"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["username"]}),
        ("Permissions", {"fields": ["is_superuser"]}),
    ]

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
