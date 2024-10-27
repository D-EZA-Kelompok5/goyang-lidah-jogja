from django.urls import path
from . import views

app_name = 'ulasGoyangan'  # Declare the app name

urlpatterns = [
    path('submit_review/<int:menu_id>/', views.submit_review, name='submit_review'),  # Review submission URL
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('menu/<int:menu_id>/comments/', views.menu_comments, name='menu_comments'),
    path('menu/<int:menu_id>/', views.menu_detail, name='menu_detail'),
    
]
