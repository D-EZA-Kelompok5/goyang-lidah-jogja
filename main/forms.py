from django.forms import ModelForm
from main.models import Menu

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['nama', 'harga', 'restoran']