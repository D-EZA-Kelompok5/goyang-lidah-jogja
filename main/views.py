from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms

# Custom User Creation Form with Role selection
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('owner', 'Restaurant Owner'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role',)


#@login_required(login_url='/login')
def show_main(request):
    context = {
        'class': 'PBP D',
        'group': '5',
        # 'last_login': request.COOKIES.get('last_login'),  # Use .get to avoid KeyError
    }
    return render(request, "main.html", context)

def register_user(request):
    form = CustomUserCreationForm()  # Gunakan CustomUserCreationForm di sini
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Menggunakan CustomUserCreationForm
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role')  # Simpan role dari form
            user.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:show_main')  # Redirect ke halaman utama setelah sukses register
    context = {'form': form}
    return render(request, 'register.html', context)

# Login user with role check
def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        selected_role = request.POST.get('role')  # Get the selected role from form
        
        # Assuming role is stored in the user model's profile or custom field
        if hasattr(user, 'role') and user.role == selected_role:  # Check if selected role matches user's role
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'You cannot login as this role.')
    
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))  # Correct namespace
    response.delete_cookie('last_login')
    return response