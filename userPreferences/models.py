from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    menus = models.ManyToManyField(
        'menuResto.Menu',
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
    menu = models.ForeignKey('menuResto.Menu', on_delete=models.CASCADE)

    class Meta:
        db_table = 'userPreferences_tag_menus'
        unique_together = ('tag', 'menu')
        managed = True
        auto_created = True
        indexes = [
            models.Index(fields=['tag', 'menu']),
        ]
