
from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Pengumuman
from .forms import PengumumanForm  


def daftar_pengumuman(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    pengumuman_list = restaurant.pengumuman.all()
    return render(request, 'daftar_pengumuman.html', {'restaurant': restaurant, 'pengumuman_list': pengumuman_list})


def tambah_pengumuman(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = PengumumanForm(request.POST)
        if form.is_valid():
            pengumuman = form.save(commit=False)
            pengumuman.restaurant = restaurant
            pengumuman.save()
            return redirect('daftar_pengumuman', restaurant_id=restaurant.id)
    else:
        form = PengumumanForm()
    return render(request, 'tambah_pengumuman.html', {'form': form, 'restaurant': restaurant})

def detail_pengumuman(request, pengumuman_id):
    pengumuman = get_object_or_404(Pengumuman, id=pengumuman_id)
    return render(request, 'detail_pengumuman.html', {'pengumuman': pengumuman})

