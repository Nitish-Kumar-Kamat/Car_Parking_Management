from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):
	username= forms.CharField(widget=forms.TextInput(attrs={'autofocus ':True,
	'class':'form-control'}))
	first_name= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email= forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	password1= forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2= forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model=User
		fields=['username','first_name','last_name','email']
		

class LoginForm(AuthenticationForm):
	username= forms.CharField(widget=forms.TextInput(attrs={'autofocus ':True,
	'class':'form-control'}))
	password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
