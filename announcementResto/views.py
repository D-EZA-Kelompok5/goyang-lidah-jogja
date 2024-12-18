from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

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