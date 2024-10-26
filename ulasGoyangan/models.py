from django.db import models
from django.conf import settings  # Import settings for referencing the user model

class Review(models.Model):
    menu = models.ForeignKey('main.Menu', on_delete=models.CASCADE, related_name='reviews')  # Reference Menu with a string
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference the user model
    rating = models.PositiveIntegerField(default=0)  # Rating field
    comment = models.TextField()  # Comment field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.menu.name}"