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
from django.db.models import Avg, Q
from ulasGoyangan.models import Review  # Import Review from ulasGoyangan
from goyangNanti.models import Wishlist
from django.contrib.auth.hashers import make_password
from goyangNanti.models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from userPreferences.models import MenuTag
from announcementResto.models import Announcement

# @login_required(login_url='/login')
def show_main(request):
    form = CustomUserCreationForm()
    menus = Menu.objects.all()
    wishlist_items = []  # Daftar kosong untuk item wishlist

    # Cek jika pengguna sudah login dan memiliki role 'CUSTOMER'
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'CUSTOMER':
        # Ambil semua ID menu di wishlist pengguna
        wishlist_items = Wishlist.objects.filter(user=request.user.profile).values_list('menu_id', flat=True)
    
    if request.user.is_authenticated:
            # Get all menus with optimized queries
        menus = Menu.objects.all().prefetch_related('tags', 'restaurant')
        
        # Get recommended menus
        user = request.user
        
        user_preference_tag_ids = user.profile.preferences.through.objects.filter(
            userprofile_id=user.profile.pk
        ).values_list('tag_id', flat=True)

        if not user_preference_tag_ids:
            recommended_menus = Menu.objects.none()
        else:
            menu_ids = MenuTag.objects.filter(
                tag_id__in=user_preference_tag_ids
            ).values_list('menu_id', flat=True)

            recommended_menus = Menu.objects.filter(
                id__in=menu_ids
            ).distinct().select_related('restaurant')

    context = {
        'form': form,
        'menus': menus,
        'wishlist_items': list(wishlist_items),  # Kirim daftar ID item wishlist ke template
        
    }

    if request.user.is_authenticated:
        context['recommended_menus'] = recommended_menus
    
    return render(request, "main.html", context)

@login_required
def main(request):
    # Get all menus with optimized queries
    menus = Menu.objects.all().prefetch_related('tags', 'restaurant')
    
    # Get recommended menus
    user = request.user
    
    user_preference_tag_ids = user.profile.preferences.through.objects.filter(
        userprofile_id=user.profile.pk
    ).values_list('tag_id', flat=True)

    if not user_preference_tag_ids:
        recommended_menus = Menu.objects.none()
    else:
        menu_ids = MenuTag.objects.filter(
            tag_id__in=user_preference_tag_ids
        ).values_list('menu_id', flat=True)

        recommended_menus = Menu.objects.filter(
            id__in=menu_ids
        ).distinct().select_related('restaurant')

    
    # Add some debugging to check what's happening
    print(f"User has preferences: {request.user.profile.preferences.exists()}")
    print(f"Number of recommended menus: {len(recommended_menus)}")
    
    context = {
        'menus': menus,
        'recommended_menus': recommended_menus,
        # 'wishlist_items': [item.menu.id for item in request.user.wishlist_set.all()],
        # Add debug info to template
        'debug_info': {
            'has_preferences': request.user.profile.preferences.exists(),
            'recommended_count': len(recommended_menus),
        }
    }

    print(context)
    
    return render(request, 'main.html', context)

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
            return redirect('main:main')
        else:
            messages.error(request, 'Username or password is incorrect!')
            return render(request, 'main.html', {'login_error': True, 'form': CustomUserCreationForm()})
    return redirect('main:show_main')

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    announcements = Announcement.objects.filter(restaurant__id=restaurant_id)
    context = {
        'restaurant': restaurant,
        'announcements': announcements
    }
    return render(request, 'restaurant_detail.html', context)

def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events.html', {'events': events})

def event_list_json(request):
    events = Event.objects.all().order_by('-date')
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

def menu_api(request):
    search_query = request.GET.get('search', '')
    
    # Use Q objects for searching in multiple fields
    if search_query:
        menus = Menu.objects.filter(
            Q(name__icontains=search_query) |  # Search in name
            Q(description__icontains=search_query) |  # Search in description
            Q(restaurant__name__icontains=search_query)  # Search in restaurant name
        )
    else:
        menus = Menu.objects.all()
    
    menu_list = []
    for menu in menus:
        menu_list.append({
            "id": menu.id,
            "name": menu.name,
            "description": menu.description,
            "price": menu.price,
            "image": menu.image,
            "restaurant": {
                "id": menu.restaurant.id,
                "name": menu.restaurant.name,
                "description": menu.restaurant.description,
                "address": menu.restaurant.address,
                "category": menu.restaurant.category,
                "price_range": menu.restaurant.price_range,
                "image": menu.restaurant.image,
                "owner": {
                    "id": menu.restaurant.owner.user.id,
                    "username": menu.restaurant.owner.user.username,
                }
            }
        })
    
    return JsonResponse({
        "menus": menu_list
    })

@csrf_exempt
@login_required
def edit_profile_api(request):
    user = request.user
    profile = user.profile
    if request.method == 'GET':
        data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': profile.bio,
            'profile_picture': profile.profile_picture,
            'role': profile.role,
            'level': profile.level,
            'review_count': profile.review_count,
            'preferences': list(profile.preferences.values()),  # Sesuaikan jika diperlukan
            'owned_restaurant': profile.owned_restaurant.name if profile.owned_restaurant else None,
            # Tambahkan field lain jika diperlukan
        }
        # print(data)  # Untuk debugging
        return JsonResponse({'status': 'success', 'data': data})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print("POST received data:", data)  # Untuk debugging
            
            # Pastikan untuk mengambil data dari key 'data'
            payload = data.get('data', {})
            
            # Update username
            user.username = payload.get('username', user.username)
            
            # Update password jika disediakan
            if payload.get('password'):
                user.set_password(payload['password'])
            
            # Update bio dan profile_picture
            profile.bio = payload.get('bio', profile.bio)
            profile.profile_picture = payload.get('profile_picture', profile.profile_picture)
            
            user.save()
            profile.save()
            
            # # Cek perubahan setelah save
            # print("After save - username:", user.username)
            # print("After save - bio:", profile.bio)
            # print("After save - profile_picture:", profile.profile_picture)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            # print("Error in POST:", e)  # Untuk debugging
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)