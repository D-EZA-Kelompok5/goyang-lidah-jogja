from django.forms import ModelForm
from .models import Menu

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'description', 'price', 'image']