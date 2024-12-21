from django import forms
from .models import Pengumuman

class PengumumanForm(forms.ModelForm):
    class Meta:
        model = Pengumuman
        fields = ['judul', 'konten']
