from django.urls import path
from .views import show_wishlist, add_wishlist, edit_wishlist, delete_wishlist, wishlist_json, create_wishlist_flutter, update_wishlist_flutter, delete_wishlist_flutter

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('add_wishlist/', add_wishlist, name='add_wishlist'),  
    path('delete_wishlist/<int:pk>/', delete_wishlist, name='delete_wishlist'),
    path('edit_wishlist/<int:pk>/', edit_wishlist, name='edit_wishlist'),
    path('create-wishlist-flutter/', create_wishlist_flutter, name='create_wishlist_flutter'),
    path('json', wishlist_json, name='wishlist_json'),
    path('update-wishlist-flutter/<int:id>/', update_wishlist_flutter, name='update_wishlist_flutter'),
    path('delete-wishlist-flutter/<int:id>/', delete_wishlist_flutter, name='delete_event_flutter'),
]