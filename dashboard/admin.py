from django.contrib import admin
from .models import Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'contact_email', 'contact_phone')
    
    def has_add_permission(self, request):
        # Allow only one instance of Settings
        if Settings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False
