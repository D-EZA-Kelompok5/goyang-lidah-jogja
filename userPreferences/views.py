from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tag
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def edit_preferences(request):
    user_profile = request.user.profile
    all_tags = Tag.objects.all().order_by('name')  # Get all tags sorted alphabetically

    if request.method == 'POST':
        # Get selected tag IDs from POST data
        selected_tag_ids = request.POST.getlist('preferences')
        # Update user's preferences
        user_profile.preferences.set(selected_tag_ids)
        messages.success(request, 'Your preferences have been updated successfully!')
        return redirect('main:main')

    # Get user's current preferences
    user_preferences = user_profile.preferences.all()

    context = {
        'all_tags': all_tags,
        'user_preferences': user_preferences,
    }
    return render(request, 'edit_preferences.html', context)

@csrf_exempt
@login_required
def api_get_all_tags(request):
    tags = Tag.objects.all().order_by('name')
    tags_data = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return JsonResponse({'tags': tags_data})

@csrf_exempt
@login_required
def user_preferences_api(request):
    if request.method == 'GET':
        # Retrieve user preferences
        user_profile = request.user.profile
        preferences = user_profile.preferences.all()
        preferences_data = [{'id': tag.id, 'name': tag.name} for tag in preferences]
        # print(preferences_data)
        return JsonResponse({
            'status': 'success',
            'data': preferences_data
        })

    elif request.method == 'POST':
        # Update user preferences
        data = json.loads(request.body)
        # print(data)
        selected_tag_ids = data.get('data', [])
        print(selected_tag_ids)
        user_profile = request.user.profile
        user_profile.preferences.set(selected_tag_ids)
        return JsonResponse({'status': 'success', 'message': 'Preferences updated successfully'})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'}, status=400)