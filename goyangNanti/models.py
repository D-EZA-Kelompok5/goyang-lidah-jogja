from django.db import models

from main.models import UserProfile
from menuResto.models import Menu

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='wishlists',
        limit_choices_to={'role': 'CUSTOMER'}
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )

    def __str__(self):
        return f"{self.user.user.username}'s wishlist item: {self.menu.name}"

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
