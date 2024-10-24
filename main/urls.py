from django.urls import path
from main.views import show_main, register_user, login_user, logout_user
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='main'),  # Landing page
    path('login/', views.login_user, name='login_user'),  # Login
    path('register/', views.register_user, name='register'),  # Register
    path('logout/', views.logout_user, name='logout'),  # Logout
    path('show_main/', views.show_main, name='show_main'),
]
