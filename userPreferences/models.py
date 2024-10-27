from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    menus = models.ManyToManyField('menuResto.Menu', related_name='tags')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
