import json
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from announcementResto.models import Announcement
from main.models import Restaurant
from menuResto.views import is_restaurant_owner
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt


# # Create your views here.
# @login_required
# @user_passes_test(is_restaurant_owner)
# def create_announcement(request, restaurant_id):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
#     # Verify ownership
#     if restaurant.owner != request.user.profile:
#         return HttpResponseForbidden("You don't have permission to create announcements for this restaurant.")
    
#     if request.method == "POST":
#         title = request.POST.get('title')
#         message = request.POST.get('message')
        
#         if title and message:
#             Announcement.objects.create(
#                 restaurant=restaurant,
#                 title=title,
#                 message=message
#             )
#             messages.success(request, 'Announcement created successfully!')
#         else:
#             messages.error(request, 'Title and message are required.')
            
#     return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant_id)

# @login_required
# @user_passes_test(is_restaurant_owner)
# def edit_announcement(request, pk):
#     announcement = get_object_or_404(Announcement, pk=pk)
#     restaurant = announcement.restaurant
    
#     # Verify ownership
#     if restaurant.owner != request.user.profile:
#         return HttpResponseForbidden("You don't have permission to edit this announcement.")
    
#     if request.method == "POST":
#         title = request.POST.get('title')
#         message = request.POST.get('message')
        
#         if title and message:
#             announcement.title = title
#             announcement.message = message
#             announcement.save()
#             messages.success(request, 'Announcement updated successfully!')
#         else:
#             messages.error(request, 'Title and message are required.')
            
#     return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant.id)

# @login_required
# @user_passes_test(is_restaurant_owner)
# def delete_announcement(request, pk):
#     announcement = get_object_or_404(Announcement, pk=pk)
#     restaurant = announcement.restaurant
    
#     # Verify ownership
#     if restaurant.owner != request.user.profile:
#         return HttpResponseForbidden("You don't have permission to delete this announcement.")
    
#     announcement.delete()
#     messages.success(request, 'Announcement deleted successfully!')
#     return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant.id)

def get_announcements(request, restaurant_id):
    try:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        print('Restaurants', restaurant)
        
        # Get filter parameter from query
        announcement_filter = request.GET.get('announcement_filter', 'newest')
        
        # Apply filter
        if announcement_filter == 'oldest':
            announcements = restaurant.announcements.all().order_by('id')
        else:  # default to newest first
            announcements = restaurant.announcements.all().order_by('-id')
        
        announcements_data = []
        for announcement in announcements:
            announcements_data.append({
                'id': announcement.id,
                'title': announcement.title,
                'message': announcement.message,
                'restaurant': {
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'description': restaurant.description,
                    'address': restaurant.address,
                    'category': restaurant.category,
                    'price_range': restaurant.price_range,
                    'image': restaurant.image,
                    'owner': {
                        'id': restaurant.owner.user.id,
                        'username': restaurant.owner.user.username,
                    }
                }
            })
        
        return JsonResponse({
            'status': 'success',
            'announcements': announcements_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def create_announcement(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if restaurant.owner != request.user.profile:
        return JsonResponse({
            "status": "error",
            "message": "You don't have permission to create announcements for this restaurant."
        }, status=403)
    
    if request.method == "POST":
        try:
            # Try to parse JSON data first
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to get POST data
                data = request.POST

            title = data.get('title')
            message = data.get('message')
            
            if not title or not message:
                return JsonResponse({
                    "status": "error",
                    "message": "Title and message are required."
                }, status=400)

            announcement = Announcement.objects.create(
                restaurant=restaurant,
                title=title,
                message=message
            )
            
            return JsonResponse({
                "status": "success",
                "announcement": {
                    "id": announcement.id,
                    "title": announcement.title,
                    "message": announcement.message,
                    "restaurant": {
                        "id": restaurant.id,
                        "name": restaurant.name,
                        "description": restaurant.description,
                        "address": restaurant.address,
                        "category": restaurant.category,
                        "price_range": restaurant.price_range,
                        "image": restaurant.image,
                        "owner": {
                            "id": restaurant.owner.user.id,
                            "username": restaurant.owner.user.username,
                        }
                    }
                }
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

@csrf_exempt
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    restaurant = announcement.restaurant
    
    if restaurant.owner != request.user.profile:
        return JsonResponse({
            "status": "error",
            "message": "You don't have permission to edit this announcement."
        }, status=403)
    
    if request.method == "POST":
        try:
            # Try to parse JSON data first
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to get POST data
                data = request.POST

            title = data.get('title')
            message = data.get('message')
            
            if not title or not message:
                return JsonResponse({
                    "status": "error",
                    "message": "Title and message are required."
                }, status=400)

            announcement.title = title
            announcement.message = message
            announcement.save()

            return JsonResponse({
                "status": "success",
                "announcement": {
                    "id": announcement.id,
                    "title": announcement.title,
                    "message": announcement.message,
                    "restaurant": {
                        "id": restaurant.id,
                        "name": restaurant.name,
                        "description": restaurant.description,
                        "address": restaurant.address,
                        "category": restaurant.category,
                        "price_range": restaurant.price_range,
                        "image": restaurant.image,
                        "owner": {
                            "id": restaurant.owner.user.id,
                            "username": restaurant.owner.user.username,
                        }
                    }
                }
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

@csrf_exempt
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    restaurant = announcement.restaurant
    
    if restaurant.owner != request.user.profile:
        return JsonResponse({
            "status": "error",
            "message": "You don't have permission to delete this announcement."
        }, status=403)
    
    announcement.delete()
    return JsonResponse({
        "status": "success",
        "message": "Announcement deleted successfully"
    })