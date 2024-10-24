from django.urls import path
from main.views import show_main, register_user, login_user, logout_user, create_menu, update_menu, delete_menu

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-menu/', create_menu, name='create_menu'),
    path('update-menu/<int:pk>/', update_menu, name='update_menu'),
    path('delete-menu/<int:pk>/', delete_menu, name='delete_menu'),
]