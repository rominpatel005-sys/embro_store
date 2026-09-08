"""
WSGI config for faction_store project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

# Load .env for local development (no-op in production where env vars are set directly)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faction_store.settings')

application = get_wsgi_application()

# Safe auto-migration on deployment (e.g. Vercel serverless)
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception:
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE orders_order ADD COLUMN IF NOT EXISTS cancel_reason TEXT;")
    except Exception:
        pass

