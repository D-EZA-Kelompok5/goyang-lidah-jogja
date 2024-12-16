from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Event
from .forms import EventForm
import json

def is_event_manager(user):
    return user.is_authenticated and user.profile.role == 'EVENT_MANAGER'

@login_required
@user_passes_test(is_event_manager)
def event_manager_dashboard(request):
    events = Event.objects.filter(created_by=request.user.profile).order_by('-date')
    return render(request, 'event_manager_dashboard.html', {'events': events})

@csrf_exempt
@login_required
@user_passes_test(is_event_manager)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user.profile
            event.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
@login_required
@user_passes_test(is_event_manager)
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
@login_required
@user_passes_test(is_event_manager)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# flutter methods

@csrf_exempt
@login_required
@user_passes_test(is_event_manager)
def create_event_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if request.user.is_authenticated:
            user_profile = request.user.profile
        else:
            return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

        title = data.get('title', '')
        description = data.get('description', '')
        date = data.get('date', '')
        time = data.get('time', '')
        location = data.get('location', '')
        entrance_fee = data.get('entrance_fee', None)

        event = Event.objects.create(
            created_by=user_profile,
            title=title,
            description=description,
            date=date,
            time=time,
            location=location,
            entrance_fee=entrance_fee,
        )
        event.save()
        return JsonResponse({"status": "success"}, status=201)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@login_required
def events_json(request):
    events = Event.objects.filter(created_by=request.user.profile)
    data = [
        {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.isoformat(),
            'time': event.time.strftime('%H:%M'),  # Memastikan format waktu yang konsisten
            'location': event.location,
            'entrance_fee': float(event.entrance_fee) if event.entrance_fee else None,  # Konversi Decimal ke float
        }
        for event in events
    ]
    # print(f'Returning {data} events for user {request.user.username}')
    return JsonResponse({'status': 'success', 'events': data}, safe=False)

@csrf_exempt
@login_required
@user_passes_test(is_event_manager)
def update_event_flutter(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            event = Event.objects.get(id=id, created_by=request.user.profile)
        except Event.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Event not found"}, status=404)

        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.date = data.get('date', event.date)
        event.time = data.get('time', event.time)
        event.location = data.get('location', event.location)
        event.entrance_fee = data.get('entrance_fee', event.entrance_fee)
        event.save()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
@login_required
@user_passes_test(is_event_manager)
def delete_event_flutter(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data.get('action') == 'delete':
                event = Event.objects.get(id=id, created_by=request.user.profile)
                event.delete()
                return JsonResponse({"status": "success"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Invalid action"}, status=400)
        except Event.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Event not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
