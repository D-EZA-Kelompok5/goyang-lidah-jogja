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
    
    context = {
        'form': form,
        'wishlist': wishlist  # Untuk menampilkan detail menu di template
    }
    return render(request, 'edit_wishlist.html', context)

@user_passes_test(is_customer)
def delete_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user.profile)
    wishlist.delete()
    return HttpResponseRedirect(reverse('wishlist:show_wishlist'))
