from django.db import models
from main.models import UserProfile
from menuResto.models import Menu

# Create your models here.
class Wishlist(models.Model):
    PILIHAN_STATUS = [
        ('BELUM', 'Belum Pernah Dibeli'),
        ('SUDAH', 'Sudah Pernah Dibeli'),
    ]

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='goyangnanti_wishlists',
        limit_choices_to={'role': 'CUSTOMER'}
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )
    catatan = models.TextField()
    status = models.CharField(
        max_length=6, 
        choices=PILIHAN_STATUS,
        default='BELUM',
    )
    
    def __str__(self):
        return f"{self.user.user.username}'s wishlist item: {self.menu.name}"

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
        unique_together = ['user', 'menu']

