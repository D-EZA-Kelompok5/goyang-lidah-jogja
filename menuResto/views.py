from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from main.models import Menu
from .forms import MenuForm

# Create your views here.

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
