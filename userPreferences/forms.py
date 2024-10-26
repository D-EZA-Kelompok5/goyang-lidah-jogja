from django import forms
from .models import Tag
from main.models import UserProfile

class UserPreferencesForm(forms.ModelForm):
    preferences = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['preferences']