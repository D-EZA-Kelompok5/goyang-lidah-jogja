from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
         return self.name

class Pengumuman(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='pengumuman')
    judul = models.CharField(max_length=200)
    konten = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul