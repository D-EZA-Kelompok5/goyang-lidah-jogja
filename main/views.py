from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Event, UserProfile
from .forms import EventForm, CustomUserCreationForm
from django.db import IntegrityError
from django.contrib.auth import get_user_model

# @login_required(login_url='/login')
def show_main(request):
    form = CustomUserCreationForm()
    context = {
        'form': form
        # 'last_login': request.COOKIES.get('last_login'),  # Use .get to avoid KeyError
    }
    return render(request, "main.html", context)

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Get the role before saving the user
                role = form.cleaned_data.get('role')
                
                # Save the user
                user = form.save()
                
                # Update the automatically created profile with the role
                user.profile.role = role
                user.profile.save()

                messages.success(request, 'Your account has been successfully created!')
                return redirect('main:show_main')

            except Exception as e:
                messages.error(request, 'An error occurred while creating your profile. Please try again.')
                return redirect('main:register')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'main.html', context)



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:show_main')
        else:
            # Pass login_error instead of using form.errors
            messages.error(request, 'Username or password is incorrect!')
            return render(request, 'main.html', {
                'login_error': True,  # Add this specific flag
                'form': CustomUserCreationForm()  # For register form
            })
    return redirect('main:show_main')


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))  # Correct namespace
    response.delete_cookie('last_login')
    return response

def is_event_manager(user):
    return user.is_authenticated and user.profile.role == 'EVENT_MANAGER'

@login_required
@user_passes_test(is_event_manager)
def event_manager_dashboard(request):
    events = Event.objects.all().order_by('-date')
    form = EventForm()
    return render(request, 'event_manager_dashboard.html', {
        'events': events,
        'form': form
    })

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

@login_required
@user_passes_test(is_event_manager)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})