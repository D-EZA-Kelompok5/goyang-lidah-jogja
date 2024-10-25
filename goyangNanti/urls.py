from django.urls import path
from .views import show_wishlist, add_wishlist, edit_wishlist, delete_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('add/', add_wishlist, name='add_wishlist'),  
    path('delete/<int:pk>/', delete_wishlist, name='delete_wishlist'),
    path('edit/<int:pk>/', edit_wishlist, name='edit_wishlist'),
]