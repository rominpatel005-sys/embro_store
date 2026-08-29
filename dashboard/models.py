from django.db import models

class Settings(models.Model):
    store_name = models.CharField(max_length=100, default="Embro Store")
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    contact_email = models.EmailField(default="support@embrostore.com")
    contact_phone = models.CharField(max_length=20, default="+1 234 567 8900")
    address = models.TextField(default="123 Embro Ave, New York, NY 10001")
    facebook_url = models.URLField(max_length=200, blank=True, default="https://facebook.com")
    instagram_url = models.URLField(max_length=200, blank=True, default="https://instagram.com")
    twitter_url = models.URLField(max_length=200, blank=True, default="https://twitter.com")

    class Meta:
        verbose_name = "Store Setting"
        verbose_name_plural = "Store Settings"

    def __str__(self):
        return self.store_name

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class DashboardWidget(models.Model):
    WIDGET_TYPES = (
        ('CARD', 'Stat Card'),
        ('CHART', 'Chart Widget'),
        ('CUSTOM', 'Custom HTML Block'),
    )
    CHART_TYPES = (
        ('PIE', 'Pie Chart'),
        ('BAR', 'Bar Chart'),
        ('LINE', 'Line Chart'),
        ('AREA', 'Area Chart'),
    )
    key = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES, default='CARD')
    
    # Custom values (if blank, computed dynamically)
    value_override = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    icon = models.CharField(max_length=100, default='fas fa-chart-bar')
    
    # Style config
    text_color = models.CharField(max_length=50, default='#ffffff')
    bg_color = models.CharField(max_length=100, default='rgba(18, 18, 22, 0.55)')
    border_color = models.CharField(max_length=100, default='rgba(255, 255, 255, 0.08)')
    
    # Chart config
    chart_type = models.CharField(max_length=20, choices=CHART_TYPES, blank=True, null=True)
    colors_json = models.TextField(default='["#d4af37", "#ffaa00", "#3b82f6", "#10b981", "#ef4444", "#a855f7"]')
    legend_visible = models.BooleanField(default=True)
    labels_json = models.TextField(blank=True, null=True) # Override datasets labels/names
    refresh_interval = models.IntegerField(default=0) # In seconds
    
    # Layout config
    is_visible = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    
    custom_html = models.TextField(blank=True, null=True)
    custom_description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-is_pinned', 'position', 'id']

    def __str__(self):
        return f"{self.title} ({self.widget_type})"

