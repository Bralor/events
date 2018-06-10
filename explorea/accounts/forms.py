from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(forms.ModelForm):
	username	= forms.CharField(max_length=30, help_text='How will we call you?')
	email		= forms.EmailField()
	first_name	= forms.CharField(max_length=100)
	last_name	= forms.CharField(max_length=100)
	password1	= forms.CharField(
			label	= "Password",
			strip	= False,
			widget	= forms.PasswordInput,
									)
	password2	= forms.CharField(
			label		= "Password",
			strip		= False,
			widget		= forms.PasswordInput,
			help_text	= "Enter the same password as before, for verification.",
									)

	class Meta:
		model = get_user_model()
		fields = [
			'username',
			'email',
			'first_name',
			'last_name',
			'password1',
			'password2',
			]

									