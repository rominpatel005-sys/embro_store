from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_superuser(sender, **kwargs):
    from django.contrib.auth.models import User
    # Automatically create the superuser admin/admin if it does not exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@embrostore.com', 'admin')
        print("--- Default Superuser 'admin' with password 'admin' auto-created ---")

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_migrate.connect(create_default_superuser, sender=self)
