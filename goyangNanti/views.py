from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Wishlist
from main.models import UserProfile
from menuResto.models import Menu
from .forms import WishlistForm

# Fungsi untuk memeriksa apakah pengguna adalah 'CUSTOMER'
def is_customer(user):
    return user.is_authenticated and user.profile.role == 'CUSTOMER'

@user_passes_test(is_customer)
def add_wishlist(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        menu_item = get_object_or_404(Menu, id=menu_id)
        user_profile = request.user.profile

        # Cek apakah item sudah ada di wishlist
        if Wishlist.objects.filter(user=user_profile, menu=menu_item).exists():
            return JsonResponse({'message': 'Item already in wishlist'}, status=400)

        # Tambah item ke wishlist
        Wishlist.objects.create(user=user_profile, menu=menu_item, catatan='', status='BELUM')
        return JsonResponse({'message': 'Item added to wishlist'}, status=200)
    
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required(login_url='/main/login')
@user_passes_test(is_customer)
def show_wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user.profile)
    context = {'wishlists': wishlists}
    return render(request, 'wishlists.html', context)

@user_passes_test(is_customer)
def edit_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user.profile)
    if request.method == 'POST':
        form = WishlistForm(request.POST, instance=wishlist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('wishlist:show_wishlist'))
    else:
        form = WishlistForm(instance=wishlist)
    
    context = {'form': form}
    return render(request, 'edit_wishlist.html', context)

@user_passes_test(is_customer)
def delete_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user.profile)
    wishlist.delete()
    return HttpResponseRedirect(reverse('wishlist:show_wishlist'))
