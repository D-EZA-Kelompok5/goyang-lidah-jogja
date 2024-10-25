from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES, 
        label='Role',
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white',
            'placeholder': 'Select Role',
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username