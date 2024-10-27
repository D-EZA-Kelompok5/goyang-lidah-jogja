from django.forms import ModelForm
from menuResto.models import Menu

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'image']