import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from userPreferences.models import Tag

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        unique=True,
        primary_key=True
    )
    ROLE_CHOICES = [
        ('EVENT_MANAGER', 'Event Manager'),
        ('RESTAURANT_OWNER', 'Restaurant Owner'),
        ('CUSTOMER', 'Customer'),
    ]
    
    LEVEL_CHOICES = [
        ('BRONZE', 'Bronze'),
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CUSTOMER'
    )
    bio = models.TextField(
        blank=True
    )
    profile_picture = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        validators=[URLValidator()]
    )
    review_count = models.PositiveIntegerField(default=0)
    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        default='BRONZE'
    )
    
    preferences = models.ManyToManyField(
        Tag,
        related_name='preferences'
    )

    def update_level(self):
        if self.review_count >= 50:
            self.level = 'GOLD'
        elif self.review_count >= 25:
            self.level = 'SILVER'
        else:
            self.level = 'BRONZE'
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price_range = models.CharField(max_length=50)
    image = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        validators=[URLValidator()]
    )
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='owned_restaurant',
        limit_choices_to={'role': 'RESTAURANT_OWNER'},
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menus'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
