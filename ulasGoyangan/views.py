# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from menuResto.models import Menu
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

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
            return redirect('main:menu_detail', menu_id=menu.id)
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
            return redirect('main:menu_detail', menu_id=review.menu.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'edit_review.html', {'form': form, 'menu': review.menu})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Ensure the user owns the review
    if request.method == 'POST':
        menu_id = review.menu.id
        review.delete()
        return redirect('main:menu_detail', menu_id=menu_id)
    
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