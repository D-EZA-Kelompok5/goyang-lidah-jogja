from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='main'),  # Landing page
    path('login/', views.login_user, name='login'),  # Login
    path('register/', views.register_user, name='register'),  # Register
    path('logout/', views.logout_user, name='logout'),  # Logout
    path('show_main/', views.show_main, name='show_main'),
    path('menu/<int:menu_id>/', views.menu_detail, name='menu_detail'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),  # Fixed name
]
