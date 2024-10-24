from django.urls import path
from main.views import show_main, register_user, login_user, logout_user, event_manager_dashboard, event_create, event_update, event_delete

app_name = 'main'

urlpatterns = [
    path('', show_main, name='main'),  # Landing page
    path('login/', login_user, name='login'),  # Login
    path('register/', register_user, name='register'),  # Register
    path('logout/', logout_user, name='logout'),  # Logout
    path('show_main/', show_main, name='show_main'),
    path('event_manager/dashboard/', event_manager_dashboard, name='event_manager_dashboard'),
    path('event_manager/events/create/', event_create, name='event_create'),
    path('event_manager/events/<int:pk>/update/', event_update, name='event_update'),
    path('event_manager/events/<int:pk>/delete/', event_delete, name='event_delete'),
]
