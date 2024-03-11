from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(max_length=50,label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length=50,label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email']
        labels = {'username':'username' ,'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                    'email':forms.EmailInput(attrs={'class':'form-control'})}