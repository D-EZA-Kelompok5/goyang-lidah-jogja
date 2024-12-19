from django.urls import path
from .views import event_manager_dashboard, event_create, event_update, event_delete, create_event_flutter, events_json, update_event_flutter, delete_event_flutter

app_name = 'managerDashboard'

urlpatterns = [
    path('', event_manager_dashboard, name='event_manager_dashboard'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:pk>/update/', event_update, name='event_update'),
    path('events/<int:pk>/delete/', event_delete, name='event_delete'),
    path('create-event-flutter/', create_event_flutter, name='create_event_flutter'),
    path('events_json/', events_json, name='user_events_json'),
    path('update-event-flutter/<int:id>/', update_event_flutter, name='update_event_flutter'),
    path('delete-event-flutter/<int:id>/', delete_event_flutter, name='delete_event_flutter'),
    ]

