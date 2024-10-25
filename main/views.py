from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import UserProfile
from .forms import CustomUserCreationForm
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from .models import Menu
from .models import Restaurant

# @login_required(login_url='/login')
def show_main(request):
    form = CustomUserCreationForm()
    menus = Menu.objects.all()
    context = {
        'form': form,
        'menus': menus,
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

def menu_detail(request, menu_id):
    # Fetch the specific menu item or return a 404 error if it doesn't exist
    menu = get_object_or_404(Menu, id=menu_id)

    # Pass the menu item to the template for rendering
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