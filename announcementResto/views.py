from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
import json
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from announcementResto.models import Announcement
from main.models import Restaurant
from menuResto.views import is_restaurant_owner
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
@login_required
@user_passes_test(is_restaurant_owner)
def create_announcement(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Verify ownership
    if restaurant.owner != request.user.profile:
        return HttpResponseForbidden("You don't have permission to create announcements for this restaurant.")

    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('message')

        if title and message:
            Announcement.objects.create(
                restaurant=restaurant,
                title=title,
                message=message
            )
            messages.success(request, 'Announcement created successfully!')
        else:
            messages.error(request, 'Title and message are required.')

    return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant_id)

@login_required
@user_passes_test(is_restaurant_owner)
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    restaurant = announcement.restaurant

    # Verify ownership
    if restaurant.owner != request.user.profile:
        return HttpResponseForbidden("You don't have permission to edit this announcement.")

    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('message')

        if title and message:
            announcement.title = title
            announcement.message = message
            announcement.save()
            messages.success(request, 'Announcement updated successfully!')
        else:
            messages.error(request, 'Title and message are required.')

    return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant.id)

@login_required
@user_passes_test(is_restaurant_owner)
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    restaurant = announcement.restaurant

    # Verify ownership
    if restaurant.owner != request.user.profile:
        return HttpResponseForbidden("You don't have permission to delete this announcement.")

    announcement.delete()
    messages.success(request, 'Announcement deleted successfully!')
    return redirect('menuResto:restaurant_detail_menu', restaurant_id=restaurant.id)

def show_announcement_json(request, restaurant_id):
    data = Announcement.objects.filter(restaurant__id=restaurant_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def api_create_announcement(request, restaurant_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)

            # Create new announcement
            announcement = Announcement.objects.create(
                restaurant=restaurant,
                title=data['title'],
                message=data['message']
            )

            return JsonResponse({
                "status": "success",
                "message": "Announcement created successfully",
                "announcement": {
                    "id": announcement.id,
                    "title": announcement.title,
                    "message": announcement.message
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)

@csrf_exempt
def api_edit_announcement(request, pk):
    if request.method == 'PUT':
        try:
            announcement = get_object_or_404(Announcement, pk=pk)
            data = json.loads(request.body)

            # Update announcement
            announcement.title = data.get('title', announcement.title)
            announcement.message = data.get('message', announcement.message)
            announcement.save()

            return JsonResponse({
                "status": "success",
                "message": "Announcement updated successfully",
                "announcement": {
                    "id": announcement.id,
                    "title": announcement.title,
                    "message": announcement.message
                }
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)

@csrf_exempt
def api_delete_announcement(request, pk):
    if request.method == 'DELETE':
        try:
            announcement = get_object_or_404(Announcement, pk=pk)
            announcement.delete()

            return JsonResponse({
                "status": "success",
                "message": "Announcement deleted successfully"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)
