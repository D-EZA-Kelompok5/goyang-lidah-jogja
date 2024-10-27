# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from menuResto.models import Menu
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from goyangNanti.models import Wishlist
from django.db.models import Avg, Count


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
    menu = get_object_or_404(Menu, id=menu_id)
    sort_option = request.GET.get('sort', 'latest')

    if sort_option == 'highest':
        reviews = menu.reviews.order_by('-rating')
    elif sort_option == 'lowest':
        reviews = menu.reviews.order_by('rating')
    elif sort_option == 'oldest':
        reviews = menu.reviews.order_by('created_at')
    else:  # Default to 'latest'
        reviews = menu.reviews.order_by('-created_at')

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