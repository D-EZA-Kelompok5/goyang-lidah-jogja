from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        unique=True
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
        max_length=500,
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    owner = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='owned_restaurant',
        limit_choices_to={'role': 'RESTAURANT_OWNER'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    entrance_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    image = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        validators=[URLValidator()]
    )
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='events',
        limit_choices_to={'role': 'EVENT_MANAGER'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    menus = models.ManyToManyField(Menu, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Announcement(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='announcements'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.restaurant.name}"

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user.username}'s wishlist item: {self.menu.name}"

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
        unique_together = ['user', 'menu']
