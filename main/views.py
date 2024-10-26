from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import UserProfile, Restaurant
from menuResto.models import Menu
from .forms import CustomUserCreationForm
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from managerDashboard.models import Event

# @login_required(login_url='/login')
def show_main(request):
    form = CustomUserCreationForm()
    menus = Menu.objects.all()
    context = {
        'form': form,
        'menus': menus,
    }
    return render(request, "main.html", context)

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                role = form.cleaned_data.get('role')
                user = form.save()
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
            messages.error(request, 'Username or password is incorrect!')
            return render(request, 'main.html', {'login_error': True, 'form': CustomUserCreationForm()})
    return redirect('main:show_main')

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response

def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {
        'menu': menu
    }
    return render(request, 'menu_detail.html', context)

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'restaurant_detail.html', context)

def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events.html', {'events': events})