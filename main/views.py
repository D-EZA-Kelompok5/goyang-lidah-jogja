from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import UserProfile, Menu, Restaurant
from .forms import CustomUserCreationForm
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from managerDashboard.models import Event
from django.db.models import Avg
from ulasGoyangan.models import Review  # Import Review from ulasGoyangan
from goyangNanti.models import Wishlist


# @login_required(login_url='/login')
def show_main(request):
    form = CustomUserCreationForm()
    menus = Menu.objects.all()
    wishlist_items = []  # Daftar kosong untuk item wishlist

    # Cek jika pengguna sudah login dan memiliki role 'CUSTOMER'
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'CUSTOMER':
        # Ambil semua ID menu di wishlist pengguna
        wishlist_items = Wishlist.objects.filter(user=request.user.profile).values_list('menu_id', flat=True)
    
    context = {
        'form': form,
        'menus': menus,
        'wishlist_items': wishlist_items,  # Kirim daftar ID item wishlist ke template
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

from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from main.models import Menu
from ulasGoyangan.models import Review

def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    
    # Calculate average rating
    reviews = Review.objects.filter(menu=menu)
    if reviews.exists():
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    else:
        average_rating = 0  # Default to 0 if no reviews

    # Pass a fixed range for stars
    star_range = [1, 2, 3, 4, 5]

    context = {
        'menu': menu,
        'average_rating': round(average_rating, 1),
        'star_range': star_range,
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