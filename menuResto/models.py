from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from main.models import Restaurant
# Create your models here.

class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menus'
    )
    menu_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        validators=[URLValidator()]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.menu_code} - {self.name} ({self.restaurant.name})"

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        unique_together = ['restaurant', 'menu_code']
        ordering = ['restaurant', 'menu_code']
