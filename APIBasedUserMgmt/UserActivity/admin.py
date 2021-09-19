from django.contrib import admin
from UserActivity.models import UserProfile, UsersActivity


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'real_name', 'time_zone',)
    search_fields = ('id', 'real_name',)


@admin.register(UsersActivity)
class UsersActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'extra_feild',)
    search_fields = ('user', 'extra_feild',)
