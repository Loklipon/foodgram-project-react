from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Follow, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'password',
                    'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'user')

    def has_add_permission(self, request, obj=None):
        return False
