from django.urls import path
from main.views import create_menu, update_menu, delete_menu

app_name = 'menuResto'

urlpatterns = [
    path('create-menu/', create_menu, name='create_menu'),
    path('update-menu/<int:pk>/', update_menu, name='update_menu'),
    path('delete-menu/<int:pk>/', delete_menu, name='delete_menu'), 
]