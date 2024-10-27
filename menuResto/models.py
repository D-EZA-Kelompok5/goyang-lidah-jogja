from django.db import models
from django.core.validators import URLValidator
# from main.models import Restaurant

class Menu(models.Model):
    restaurant = models.ForeignKey(
        'main.Restaurant',
        on_delete=models.CASCADE,
        related_name='menus'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.PositiveBigIntegerField()
    image = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        validators=[URLValidator()]
    )

    def __str__(self):        
        return f"{self.name} ({self.restaurant.name})"

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'