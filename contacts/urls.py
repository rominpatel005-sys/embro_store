from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contact_view, name='contact_page'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
