from django.urls import path
from . import views

app_name = 'announcementResto'

urlpatterns = [
    path('announcement/<int:restaurant_id>/create/', views.create_announcement, name='create_announcement'),
    path('announcement/<int:pk>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcement/<int:pk>/delete/', views.delete_announcement, name='delete_announcement'),
    # path('restoran/<int:restaurant_id>/pengumuman/', views.daftar_pengumuman, name='daftar_pengumuman'),
    # path('restoran/<int:restaurant_id>/pengumuman/tambah/', views.tambah_pengumuman, name='tambah_pengumuman'),
    # path('pengumuman/<int:pengumuman_id>/', views.detail_pengumuman, name='detail_pengumuman'),
]
