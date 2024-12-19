from django.urls import path
from . import views

app_name = 'announcementResto'

urlpatterns = [
    path('announcement/<int:restaurant_id>/create/', views.create_announcement, name='create_announcement'),
    path('announcement/<int:pk>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcement/<int:pk>/delete/', views.delete_announcement, name='delete_announcement'),

    path('announcement/json/<int:restaurant_id>', views.show_announcement_json, name='show_json'),
    path('api/announcement/<int:restaurant_id>/create/', views.api_create_announcement, name='api_create_announcement'),
    path('api/announcement/<int:pk>/edit/', views.api_edit_announcement, name='api_edit_announcement'),
    path('api/announcement/<int:pk>/delete/', views.api_delete_announcement, name='api_delete_announcement'),
]
