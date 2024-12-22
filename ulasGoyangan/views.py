from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Review
from menuResto.models import Menu
from goyangNanti.models import Wishlist
from django.db.models import Avg, Count
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect



@csrf_exempt
@login_required
def submit_review_json(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    if request.method == 'POST':
        try:
            # Ambil data form-encoded
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            # Debugging: Tampilkan data yang diterima
            print(f"Received rating: {rating}, comment: {comment}")

            # Validasi data
            if rating is None or comment is None:
                raise ValueError("Rating dan komentar harus disertakan.")

            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError("Rating harus antara 1 hingga 5.")
            except ValueError:
                raise ValueError("Rating harus berupa angka antara 1 hingga 5.")

            if not comment.strip():
                raise ValueError("Komentar tidak boleh kosong.")

            # Buat objek Review
            review = Review.objects.create(
                menu=menu,
                user=request.user,  # Assign User instance
                rating=rating,
                comment=comment,
            )

            # Debugging: Tampilkan ID review yang dibuat
            print(f"Review created with ID: {review.id}")

            return JsonResponse({
                'message': 'Review submitted successfully',
                'review': {
                    'id': review.id,
                    'menu_id': menu.id,
                    'user': review.user.username,
                    'rating': review.rating,
                    'comment': review.comment,
                    'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }, status=201)

        except ValueError as ve:
            # Debugging: Tampilkan error
            print(f"ValueError: {ve}")
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            # Debugging: Tampilkan error
            print(f"Exception: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
@login_required
def edit_review_json(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        try:
            # Ambil data form-encoded
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            # Debugging: Tampilkan data yang diterima
            print(f"Received rating: {rating}, comment: {comment}")

            # Validasi data
            if rating is None or comment is None:
                raise ValueError("Rating dan komentar harus disertakan.")

            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError("Rating harus antara 1 hingga 5.")
            except ValueError:
                raise ValueError("Rating harus berupa angka antara 1 hingga 5.")

            if not comment.strip():
                raise ValueError("Komentar tidak boleh kosong.")

            # Update objek Review
            review.rating = rating
            review.comment = comment
            review.save()

            # Debugging: Tampilkan review yang diperbarui
            print(f"Review updated: {review.id}, rating: {review.rating}, comment: {review.comment}")

            return JsonResponse({
                'message': 'Review updated successfully',
                'review': {
                    'id': review.id,
                    'menu_id': review.menu.id,
                    'user': request.user.username,
                    'rating': review.rating,
                    'comment': review.comment,
                    'last_edited': review.updated_at.strftime('%Y-%m-%d %H:%M:%S') if review.updated_at else None,
                }
            }, status=200)
        except ValueError as ve:
            # Debugging: Tampilkan error
            print(f"ValueError: {ve}")
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            # Debugging: Tampilkan error
            print(f"Exception: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@login_required
def delete_review_json(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'DELETE':
        try:
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def my_reviews_json(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    reviews_data = [{
        'id': review.id,
        'menu_id': review.menu.id,
        'menu_name': review.menu.name,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    } for review in reviews]
    return JsonResponse({
        'reviews': reviews_data,
        'review_count': reviews.count(),
    }, status=200)

def menu_comments_json(request, menu_id):
    reviews = Review.objects.filter(menu_id=menu_id)
    rating = request.GET.get('rating')
    sort_option = request.GET.get('sort')

    if rating:
        reviews = reviews.filter(rating=int(rating))

    if sort_option == 'highest':
        reviews = reviews.order_by('-rating')
    elif sort_option == 'lowest':
        reviews = reviews.order_by('rating')
    elif sort_option == 'latest':
        reviews = reviews.order_by('-created_at')
    elif sort_option == 'oldest':
        reviews = reviews.order_by('created_at')

    reviews_data = [{
        'id': review.id,
        'user': review.user.username,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    } for review in reviews]
    return JsonResponse({'reviews': reviews_data}, status=200)

def menu_detail_json(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    reviews = Review.objects.filter(menu=menu)

    if reviews.exists():
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(average_rating, 1)
    else:
        average_rating = 0

    total_reviews = reviews.count()
    rating_counts = reviews.values('rating').annotate(count=Count('rating'))
    rating_distribution = {str(i): 0 for i in range(1, 6)}

    for item in rating_counts:
        rating_distribution[str(item['rating'])] = item['count']

    menu_data = {
        'id': menu.id,
        'name': menu.name,
        'description': menu.description,
        'price': menu.price,
        'image': menu.image.url if menu.image else None,
        'restaurant': {
            'id': menu.restaurant.id,
            'name': menu.restaurant.name,
            'address': menu.restaurant.address,
        },
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'rating_distribution': rating_distribution,
    }
    return JsonResponse(menu_data, status=200)

#-----------------------------------------------------------------------------------------------------------------------------
@login_required
def submit_review(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.menu = menu
            review.user = request.user
            review.save()
            return redirect('ulasGoyangan:menu_detail', menu_id=menu.id)
    else:
        form = ReviewForm()

    return render(request, 'submit_review.html', {'form': form, 'menu': menu})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Ensure the user owns the review
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('ulasGoyangan:menu_detail', menu_id=review.menu.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'edit_review.html', {'form': form, 'menu': review.menu})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Ensure the user owns the review
    if request.method == 'POST':
        menu_id = review.menu.id
        review.delete()
        return redirect('ulasGoyangan:menu_detail', menu_id=menu_id)
    
    return render(request, 'delete_review.html', {'review': review})

@login_required
def my_reviews(request):
    user_reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    review_count = user_reviews.count()
    
    # Update the review count in UserProfile
    profile = request.user.profile
    profile.review_count = review_count
    profile.update_level()  # Update level based on the new review count
    
    return render(request, 'my_reviews.html', {
        'user_reviews': user_reviews,
        'review_count': review_count,
        'level': profile.level
    })

def menu_comments(request, menu_id):
    reviews = Review.objects.filter(menu_id=menu_id)
    
    # Mendapatkan parameter filter dan sort dari permintaan GET
    rating = request.GET.get('rating')
    sort_option = request.GET.get('sort')

    # Filter berdasarkan rating
    if rating:
        reviews = reviews.filter(rating=int(rating))

    # Sort berdasarkan opsi yang dipilih
    if sort_option == 'highest':
        reviews = reviews.order_by('-rating')
    elif sort_option == 'lowest':
        reviews = reviews.order_by('rating')
    elif sort_option == 'latest':
        reviews = reviews.order_by('-created_at')
    elif sort_option == 'oldest':
        reviews = reviews.order_by('created_at')

    return render(request, 'partials/comments_section.html', {'reviews': reviews})

def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)

    # Get all reviews for the menu
    reviews = Review.objects.filter(menu=menu)

    # Calculate average rating
    if reviews.exists():
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(average_rating, 1)
    else:
        average_rating = 0  # Default to 0 if no reviews

    # Calculate rating distribution
    total_reviews = reviews.count()
    rating_counts = reviews.values('rating').annotate(count=Count('rating'))
    rating_distribution = {'5': 0, '4': 0, '3': 0, '2': 0, '1': 0}

    for item in rating_counts:
        rating = str(item['rating'])
        count = item['count']
        percentage = (count / total_reviews) * 100
        rating_distribution[rating] = round(percentage, 2)

    # Pass a fixed range for stars
    star_range = [1, 2, 3, 4, 5]

    is_wishlisted = Wishlist.objects.filter(user=request.user.profile, menu=menu).exists() if request.user.is_authenticated else False
    
    context = {
        'menu': menu,
        'average_rating': average_rating,
        'star_range': star_range,
        'rating_distribution': rating_distribution,  # Add this line
        'is_wishlisted' : is_wishlisted,
    }
    return render(request, 'menu_detail.html', context)