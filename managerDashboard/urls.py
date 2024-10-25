from django.urls import path
from .views import event_manager_dashboard, event_create, event_update, event_delete

app_name = 'managerDashboard'

urlpatterns = [
    path('', event_manager_dashboard, name='event_manager_dashboard'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:pk>/update/', event_update, name='event_update'),
    path('events/<int:pk>/delete/', event_delete, name='event_delete'),
    ]

