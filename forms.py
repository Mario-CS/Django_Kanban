from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Board, Column, Card


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-input'
        self.fields['password2'].widget.attrs['class'] = 'form-input'


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Contraseña'}))


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name", "description"]


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ["board", "name", "position"]


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["column", "title", "description", "position"]
