from django.urls import path
from . import views

app_name = 'userPreferences'

urlpatterns = [
    path('edit/', views.edit_preferences, name='edit_preferences'),
    path('api/tags/', views.api_get_all_tags, name='api_get_all_tags'),
    path('api/preferences/', views.user_preferences_api, name='user_preferences_api'),
]