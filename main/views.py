from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import UserProfile, Restaurant
from menuResto.models import Menu
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from managerDashboard.models import Event
from django.db.models import Avg
from ulasGoyangan.models import Review  # Import Review from ulasGoyangan
from goyangNanti.models import Wishlist
from django.db.models import Avg, Count
from django.contrib.auth.hashers import make_password
from django.db.models import Avg, Count
from announcementResto.models import Announcement

from goyangNanti.models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

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
        'wishlist_items': list(wishlist_items),  # Kirim daftar ID item wishlist ke template
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

    # Get all reviews for the menu
    reviews = Review.objects.filter(menu=menu)

    # Calculate average rating
    if reviews.exists():
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(average_rating, 1)
    else:
        average_rating = 0  # Default to 0 if no reviews

    # Calculate rating distribution
    total_reviews = reviews.count()
    rating_counts = reviews.values('rating').annotate(count=Count('rating'))
    rating_distribution = {'5': 0, '4': 0, '3': 0, '2': 0, '1': 0}

    for item in rating_counts:
        rating = str(item['rating'])
        count = item['count']
        percentage = (count / total_reviews) * 100
        rating_distribution[rating] = round(percentage, 2)

    # Pass a fixed range for stars
    star_range = [1, 2, 3, 4, 5]

    is_wishlisted = Wishlist.objects.filter(user=request.user.profile, menu=menu).exists() if request.user.is_authenticated else False
    
    context = {
        'menu': menu,
        'average_rating': average_rating,
        'star_range': star_range,
        'rating_distribution': rating_distribution,  # Add this line
        'is_wishlisted' : is_wishlisted,
    }
    return render(request, 'menu_detail.html', context)

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    announcements = Announcement.objects.filter(restaurant__owner_id=request.user.id)
    context = {
        'restaurant': restaurant,
        'announcements': announcements
    }
    return render(request, 'restaurant_detail.html', context)

def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events.html', {'events': events})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Handle password update if provided
            password = user_form.cleaned_data.get('password')
            if password:
                request.user.password = make_password(password)
            
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('main:edit_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    # Get restaurant information if user is a restaurant owner
    owned_restaurant = None
    if request.user.profile.role == 'RESTAURANT_OWNER':
        owned_restaurant = request.user.profile.owned_restaurant.first()
    
    request.user.profile.update_level()

    context = {
        'user': request.user,
        'user_profile': request.user.profile,
        'owned_restaurant': owned_restaurant,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'edit_profile.html', context)

def goyang_nanti(request):
    return render(request, 'goyang_nanti.html')

def ulas_goyangan(request):
    return render(request, 'ulas_goyangan.html')

def event_dashboard(request):
    return render(request, 'event_dashboard.html')

def menu_resto(request):
    return render(request, 'menu_resto.html')

def annoucement_resto(request):
    return render(request, 'annoucement_resto.html')

def menu_comments(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    sort_option = request.GET.get('sort', 'latest')

    if sort_option == 'highest':
        reviews = menu.reviews.order_by('-rating')
    elif sort_option == 'lowest':
        reviews = menu.reviews.order_by('rating')
    elif sort_option == 'oldest':
        reviews = menu.reviews.order_by('created_at')
    else: 
        reviews = menu.reviews.order_by('-created_at')

    return render(request, 'partials/comments_section.html', {'reviews': reviews})
