from django.urls import path
from . import views

app_name = 'menuResto'

urlpatterns = [
    path('', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('o/<int:restaurant_id>/', views.restaurant_detail_menu, name='restaurant_detail_menu'),
    path('<int:restaurant_id>/create-menu/', views.create_menu, name='create_menu'),
    path('edit-menu/<int:pk>/', views.edit_menu, name='edit_menu'),
    path('delete-menu/<int:pk>/', views.delete_menu, name='delete_menu'),
]