from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from api.posts.models import Post
from api.users.models import UserProfile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'timestamp']
    list_filter = ['timestamp', 'user']
    search_fields = ['message', 'user__username']
    readonly_fields = ['timestamp']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_email_verified', 'email_verification_sent_at']
    list_filter = ['is_email_verified']
    search_fields = ['user__username', 'user__email']

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
