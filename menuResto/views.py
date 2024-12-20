import json
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from announcementResto.models import Announcement
from main.models import Restaurant
from .forms import MenuForm
from django.db.models import Q
from menuResto.models import Menu
from django.views.decorators.csrf import csrf_exempt

def is_restaurant_owner(user):
    return user.is_authenticated and user.profile.role == 'RESTAURANT_OWNER'

@login_required
@user_passes_test(is_restaurant_owner)
def restaurant_dashboard(request):
    # Get all restaurants owned by the current user's profile
    restaurants = Restaurant.objects.filter(owner_id=request.user.id)
    context = {'restaurants': restaurants}
    return render(request, 'restaurant_dashboard.html', context)

from django.http import JsonResponse

# @user_passes_test(is_restaurant_owner)
def restaurant_dashboard_api(request):
    restaurants = Restaurant.objects.filter(owner_id=request.user.id)
    data = [{
        'id': restaurant.id,
        'name': restaurant.name,
        'description': restaurant.description,
        'address': restaurant.address,
        'category': restaurant.category,
        'price_range': restaurant.price_range.split(' ')[0],
        'image': restaurant.image,
        'owner': {
            'id': restaurant.owner.user.id,
            'username': restaurant.owner.user.username,
        }
    } for restaurant in restaurants]

    print(data)
    return JsonResponse({'restaurants': data})

@login_required
@user_passes_test(is_restaurant_owner)
def restaurant_detail_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    # Check ownership
    if restaurant.owner != request.user.profile:
        return HttpResponseForbidden("You don't have permission to access this restaurant.")
    
    # Get filter parameters
    menu_filter = request.GET.get('menu_filter', 'all')
    announcement_filter = request.GET.get('announcement_filter', 'all')
    
    # Filter menus
    menus = Menu.objects.filter(restaurant_id=restaurant.id)
    if menu_filter == 'price_low':
        menus = menus.order_by('price')
    elif menu_filter == 'price_high':
        menus = menus.order_by('-price')
    elif menu_filter == 'name_asc':
        menus = menus.order_by('name')
    elif menu_filter == 'name_desc':
        menus = menus.order_by('-name')
    
    # Filter announcements
    announcements = restaurant.announcements.all()
    if announcement_filter == 'newest':
        announcements = announcements.order_by('-id')
    elif announcement_filter == 'oldest':
        announcements = announcements.order_by('id')
    
    context = {
        'restaurant': restaurant,
        'menus': menus,
        'announcements': announcements,
        'menu_filter': menu_filter,
        'announcement_filter': announcement_filter,
    }
    return render(request, 'restaurant_detail_menu.html', context)

from django.http import JsonResponse

# @login_required
# @user_passes_test(is_restaurant_owner)
def restaurant_detail_menu_api(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    # Check ownership
    if restaurant.owner != request.user.profile:
        return JsonResponse({"error": "You don't have permission to access this restaurant."}, status=403)
    
    # Get filter parameters
    menu_filter = request.GET.get('menu_filter', 'all')
    
    # Filter menus
    menus = Menu.objects.filter(restaurant_id=restaurant.id)
    if menu_filter == 'price_low':
        menus = menus.order_by('price')
    elif menu_filter == 'price_high':
        menus = menus.order_by('-price')
    elif menu_filter == 'name_asc':
        menus = menus.order_by('name')
    elif menu_filter == 'name_desc':
        menus = menus.order_by('-name')
    
    # Serialize restaurant data
    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'description': restaurant.description,
        'address': restaurant.address,
        'category': restaurant.category,
        'price_range': restaurant.price_range.split(' ')[0],
        'image': restaurant.image,
        'owner': {
            'id': restaurant.owner.user.id,
            'username': restaurant.owner.user.username,
        }
    }

    print("Restaurant data being sent:", restaurant_data)
    
    # Serialize menu data
    menus_data = [{
        'id': menu.id,
        'name': menu.name,
        'description': menu.description,
        'price': menu.price,
        'image': menu.image,
        'restaurant': restaurant_data
    } for menu in menus]
    
    # print(menus_data)

    return JsonResponse({
        'restaurant': restaurant_data,
        'menus': menus_data
    })

@login_required
@user_passes_test(is_restaurant_owner)
def create_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    # Verify ownership
    if restaurant.owner != request.user.profile:
        return HttpResponseForbidden("You don't have permission to add menus to this restaurant.")
    
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.restaurant = restaurant
            menu.save()
            messages.success(request, 'Menu item created successfully!')
            return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant_id)
    else:
        form = MenuForm()
    
    context = {
        'form': form,
        'restaurant': restaurant,
        'action': 'Create'
    }
    return render(request, 'create_menu.html', context)

@login_required
@user_passes_test(is_restaurant_owner)
def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    restaurant = menu.restaurant
    
    # Verify ownership
    if restaurant.owner != request.user.profile:
        return HttpResponseForbidden("You don't have permission to edit this menu.")
    
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant.id)
    else:
        form = MenuForm(instance=menu)
    
    context = {
        'form': form,
        'menu': menu,
        'restaurant': restaurant,
        'action': 'Edit'
    }
    return render(request, 'edit_menu.html', context)

@login_required
@user_passes_test(is_restaurant_owner)
def delete_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    
    restaurant = menu.restaurant
    
    # Verify ownership
    if restaurant.owner != request.user.profile:
        return HttpResponseForbidden("You don't have permission to delete this menu.")
    
    menu.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant.id)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json
from django.views.decorators.http import require_http_methods

@csrf_exempt
def create_menu_api(request, restaurant_id):
    if request.method != "POST":
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST method is allowed'
        }, status=405)
    
    try:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        
        # Verify ownership
        if restaurant.owner != request.user.profile:
            return JsonResponse({
                'status': 'error',
                'message': 'You do not have permission to add menus to this restaurant'
            }, status=403)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST
            
        # Create new menu
        menu = Menu(
            name=data.get('name'),
            description=data.get('description'),
            price=float(data.get('price', 0)),
            image=data.get('image'),
            restaurant=restaurant
        )
        
        # Validate and save
        menu.full_clean()
        menu.save()
        
        # Return response in the same format expected by MenuElement.fromJson
        response_data = {
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'price': menu.price,
            'image': menu.image,
            'restaurant': {
                'id': restaurant.id,
                'name': restaurant.name,
                'description': restaurant.description,
                'address': restaurant.address,
                'category': restaurant.category,
                'price_range': restaurant.price_range.split(' ')[0],
                'image': restaurant.image,
                'owner': {
                    'id': restaurant.owner.user.id,
                    'username': restaurant.owner.user.username,
                }
            },
            'tags': []  # Empty tags for new menu
        }
        
        return JsonResponse(response_data)
        
    except ValidationError as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Validation error',
            'errors': dict(e)
        }, status=400)
    except Exception as e:
        print(f"Error in create_menu_api: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def edit_menu_api(request, pk):
    try:
        menu = get_object_or_404(Menu, pk=pk)
        restaurant = menu.restaurant
        
        # Verify ownership
        if restaurant.owner != request.user.profile:
            return JsonResponse({
                'status': 'error',
                'message': 'You do not have permission to edit this menu'
            }, status=403)
        
        # Parse request data
        try:
            # First try to parse as JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to get POST data
            data = request.POST

        # Ensure we have valid data
        if not data:
            return JsonResponse({
                'status': 'error',
                'message': 'No data provided'
            }, status=400)

        # Print received data for debugging
        print("Received data:", data)
        
        # Update menu fields
        if 'name' in data:
            menu.name = data['name']
        if 'description' in data:
            menu.description = data['description']
        if 'price' in data:
            try:
                menu.price = float(data['price'])  # Convert price to float
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid price format'
                }, status=400)
        if 'image' in data:
            menu.image = data['image']
        
        # Validate and save
        try:
            menu.full_clean()
            menu.save()
        except ValidationError as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Validation error',
                'errors': dict(e)
            }, status=400)
        
        # Return updated menu data
        return JsonResponse({
            'status': 'success',
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'price': menu.price,
            'image': menu.image,
            'restaurant': {
                'id': restaurant.id,
                'name': restaurant.name,
                'description': restaurant.description,
                'address': restaurant.address,
                'category': restaurant.category,
                'price_range': restaurant.price_range.split(' ')[0],
                'image': restaurant.image,
                'owner': {
                    'id': restaurant.owner.user.id,
                    'username': restaurant.owner.user.username,
                }
            }
        })
        
    except Exception as e:
        print(f"Error in edit_menu_api: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def delete_menu_api(request, pk):
    # Accept both POST and DELETE methods
    if request.method not in ["POST", "DELETE"]:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST or DELETE method is allowed'
        }, status=405)
    
    try:
        menu = get_object_or_404(Menu, pk=pk)
        restaurant = menu.restaurant
        
        # Verify ownership
        if restaurant.owner != request.user.profile:
            return JsonResponse({
                'status': 'error',
                'message': 'You do not have permission to delete this menu'
            }, status=403)
        
        # Store menu info before deletion for response
        menu_id = menu.id
        restaurant_id = restaurant.id
        
        # Delete the menu
        menu.delete()
        
        response = JsonResponse({
            'status': 'success',
            'message': 'Menu deleted successfully',
            'menu_id': menu_id,
            'restaurant_id': restaurant_id
        })
        
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
        
        return response
        
    except Menu.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Menu not found'
        }, status=404)
    except Exception as e:
        print(f"Error in delete_menu_api: {str(e)}")  # Add debugging
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)