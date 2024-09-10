from django import forms
from .models import Song
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']