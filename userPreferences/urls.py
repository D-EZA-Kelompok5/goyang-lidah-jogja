from django.urls import path
from . import views

app_name = 'userPreferences'

urlpatterns = [
    path('edit/', views.edit_preferences, name='edit_preferences'),
]