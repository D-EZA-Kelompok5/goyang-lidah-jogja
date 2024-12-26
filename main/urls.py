from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),  # Landing page
    path('login/', views.login_user, name='login'),  # Login
    path('register/', views.register_user, name='register'),  # Register
    path('logout/', views.logout_user, name='logout'),  # Logout
    path('main/', views.main, name='main'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'), 
    path('events/', views.event_list, name='event_list'), 
    path('events_json/', views.event_list_json, name='event_list_json'), 
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('goyang_nanti', views.goyang_nanti, name='goyang_nanti'),
    path('ulas_goyangan', views.ulas_goyangan, name='ulas_goyangan'),
    path('menu_resto', views.menu_resto, name='menu_resto'),
    path('event_dashboard', views.event_dashboard, name='event_dashboard'),
    path('annoucement_resto', views.annoucement_resto, name='annoucement_resto'),
]
