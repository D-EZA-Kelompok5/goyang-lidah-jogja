from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Review
from menuResto.models import Menu
from goyangNanti.models import Wishlist
from django.db.models import Avg, Count
import json
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@login_required
def submit_review(request, menu_id):
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
def edit_review(request, review_id):
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
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'DELETE':
        try:
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def my_reviews(request):
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

def menu_comments(request, menu_id):
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

def menu_detail(request, menu_id):
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

