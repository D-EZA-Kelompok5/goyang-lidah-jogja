from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Wishlist
from main.models import UserProfile
from menuResto.models import Menu
from .forms import WishlistForm
import json
from django.views.decorators.http import require_http_methods

# Fungsi untuk memeriksa apakah pengguna adalah 'CUSTOMER'
def is_customer(user):
    return user.is_authenticated and user.profile.role == 'CUSTOMER'

@require_http_methods(["POST"])
@user_passes_test(is_customer)
def add_wishlist(request):
    try:
        data = json.loads(request.body)
        menu_id = data.get('menu_id')
        
        if not menu_id:
            return JsonResponse({'message': 'Menu ID is required'}, status=400)
            
        menu_item = get_object_or_404(Menu, id=menu_id)
        user_profile = request.user.profile

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user_profile,
            menu=menu_item,
            defaults={
                'catatan': '',  # Set default empty note
                'status': 'BELUM'
            }
        )

        if created:
            return JsonResponse({
                'status': 'added',
                'message': 'Item added to wishlist'
            })
        else:
            wishlist_item.delete()
            return JsonResponse({
                'status': 'removed',
                'message': 'Item removed from wishlist'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@login_required(login_url='/main/login')
@user_passes_test(is_customer)
def show_wishlist(request):
    user_profile = request.user.profile
    wishlists = Wishlist.objects.filter(user=user_profile)

    # Ambil nilai filter dari request GET
    sort_order = request.GET.get('sort_order')
    price_range = request.GET.get('price_range')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter berdasarkan range harga tetap
    if price_range == 'under_20000':
        wishlists = wishlists.filter(menu__price__lt=20000)
    elif price_range == '20000_40000':
        wishlists = wishlists.filter(menu__price__gte=20000, menu__price__lte=40000)
    elif price_range == '40000_60000':
        wishlists = wishlists.filter(menu__price__gte=40000, menu__price__lte=60000)
    elif price_range == '60000_80000':
        wishlists = wishlists.filter(menu__price__gte=60000, menu__price__lte=80000)
    elif price_range == '80000_100000':
        wishlists = wishlists.filter(menu__price__gte=80000, menu__price__lte=100000)
    elif price_range == '100000_150000':
        wishlists = wishlists.filter(menu__price__gte=100000, menu__price__lte=150000)
    elif price_range == '150000_200000':
        wishlists = wishlists.filter(menu__price__gte=150000, menu__price__lte=200000)
    elif price_range == 'above_200000':
        wishlists = wishlists.filter(menu__price__gt=200000)

    # Filter berdasarkan harga minimum dan maksimum jika ada
    if min_price:
        wishlists = wishlists.filter(menu__price__gte=min_price)
    if max_price:
        wishlists = wishlists.filter(menu__price__lte=max_price)

    # Pengurutan berdasarkan harga
    if sort_order == 'ascending':
        wishlists = wishlists.order_by('menu__price')
    elif sort_order == 'descending':
        wishlists = wishlists.order_by('-menu__price')

    context = {
        'wishlists': wishlists,
    }
    return render(request, 'wishlists.html', context)

@user_passes_test(is_customer)
def edit_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user.profile)
    if request.method == 'POST':
        form = WishlistForm(request.POST, instance=wishlist)
        if form.is_valid():
            form.save()
            
            # Respon JSON dengan informasi lengkap untuk frontend
            return JsonResponse({
                'status': 'success',
                'message': 'Wishlist item updated successfully.',
                'catatan': form.cleaned_data['catatan'],
                'status_display': wishlist.get_status_display(),
                'redirect_url': reverse('wishlist:show_wishlist')  # URL tujuan untuk redirect
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Form data is invalid.'}, status=400)
    else:
        form = WishlistForm(instance=wishlist)
    
    context = {
        'form': form,
        'wishlist': wishlist
    }
    return render(request, 'edit_wishlist.html', context)

@user_passes_test(is_customer)
def delete_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user.profile)
    wishlist.delete()
    return HttpResponseRedirect(reverse('wishlist:show_wishlist'))
