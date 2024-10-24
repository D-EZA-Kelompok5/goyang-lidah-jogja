from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required(login_url='/login')
def show_main(request):
    context = {
        'class': 'PBP D',
        'group': '5',
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def create_menu(request):
    form = MenuForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        menu_entry = form.save(commit=False)
        menu_entry.user = request.user
        menu_entry.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, 'create_menu.html', context)

def edit_menu(request, pk):
    target = Menu.objects.get(pk=pk)

    if request.method == "POST":
        form = MenuForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:show_main'))
        context = {'form': form}
        return render(request, 'edit_menu.html', context)

def delete_menu(request, pk):
    menu = Menu.objects.get(pk=pk)
    menu.delete()
    return HttpResponseRedirect(reverse('main:show_main'))