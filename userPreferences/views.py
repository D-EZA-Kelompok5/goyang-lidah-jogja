from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserPreferencesForm
from .models import Tag

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