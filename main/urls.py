from django.urls import path
from main.views import show_main, register_user, login_user, logout_user

app_name = 'main'

urlpatterns = [
    path('', show_main, name='main'),  # Landing page
    path('login/', login_user, name='login'),  # Login
    path('register/', register_user, name='register'),  # Register
    path('logout/', logout_user, name='logout'),  # Logout
    path('show_main/', show_main, name='show_main'),
    ]