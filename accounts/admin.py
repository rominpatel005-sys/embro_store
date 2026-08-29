from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'city', 'state', 'email_verified')
    search_fields = ('user__username', 'user__email', 'mobile', 'city')
    list_filter = ('email_verified', 'state')
