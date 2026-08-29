from dashboard.models import Settings

def store_settings(request):
    return {
        'store_settings': Settings.get_settings()
    }
