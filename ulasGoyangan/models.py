from django.db import models
from django.conf import settings  # Import settings for referencing the user model
from django.utils import timezone
from menuResto.models import Menu

# Create your models here.
class Review(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews')  # Reference Menu with a string
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference the user model
    rating = models.PositiveIntegerField(default=0)  # Rating field
    comment = models.TextField()  # Comment field
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(null=True, blank=True)  # New field

    def __str__(self):
        return f"Review by {self.user.username} for {self.menu.name}"
    
    def save(self, *args, **kwargs):
        if self.pk:  # Only update last_edited if the review is being edited (exists)
            self.last_edited = timezone.now()
        super().save(*args, **kwargs)