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

def is_restaurant_owner(user):
    return user.is_authenticated and user.profile.role == 'RESTAURANT_OWNER'

@login_required
@user_passes_test(is_restaurant_owner)
def restaurant_dashboard(request):
    # Get all restaurants owned by the current user's profile
    restaurants = Restaurant.objects.filter(owner_id=request.user.id)
    context = {'restaurants': restaurants}
    return render(request, 'restaurant_dashboard.html', context)

@login_required
@user_passes_test(is_restaurant_owner)
def restaurant_detail_menu(request, restaurant_id):
    # Get the restaurant and verify ownership
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    # Check if the current user owns this restaurant
    if restaurant.owner != request.user.profile:
        return HttpResponseForbidden("You don't have permission to access this restaurant.")
    
    # Get all menus for this restaurant
    menus = Menu.objects.filter(restaurant_id=restaurant.id)
    
    # Get announcements for this restaurant, ordered by most recent
    announcements = restaurant.announcements.all().order_by('-id')
    
    context = {
        'restaurant': restaurant,
        'menus': menus,
        'announcements': announcements,
    }
    return render(request, 'restaurant_detail_menu.html', context)

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