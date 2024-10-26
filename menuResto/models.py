from django.db import models
from django.core.validators import URLValidator
from main.models import Restaurant

class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
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

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    menus = models.ManyToManyField(
        Menu,
        through='MenuTag',
        related_name='tags'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class MenuTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = 'menuResto_tag_menus'
        unique_together = ('tag', 'menu')
        managed = True
        auto_created = True
        indexes = [
            models.Index(fields=['tag', 'menu']),
        ]