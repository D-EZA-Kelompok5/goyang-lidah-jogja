from django.db import models
from main.models import Restaurant

# Create your models here.
class Announcement(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='announcements'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.restaurant.name}"

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'