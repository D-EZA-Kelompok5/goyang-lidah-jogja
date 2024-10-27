from .models import Review

def review_count(request):
    if request.user.is_authenticated:
        count = Review.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'review_count': count}