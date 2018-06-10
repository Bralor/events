from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

def profile(request):
	return render(request, 'accounts/profile.html')

def register(request):
	if request.method == 'POST':
		# Create thte form and populate it with data from the POST request
		form = RegisterForm(request.POST)

		# Validate the data in the form
		if form.is_valit():
			user = form.save()
			raw_password = form.cleaned_data.get('password1')

			# Get the validated data from the form
			# username	= form.cleaned_data,get('username')
			# email		= form.cleaned_data.get('email')
			# first_name	= form.cleaned_data.get('first_name')
			# last_name	= form.cleaned_data.get('last_name')
			# password	= form.cleaned_data.get('password1')

			# Craete and save the user
			# User = get_user_model()
			# u = User(
			# 	username=username,
			# 	email=email,
			# 	first_name=first_name,
			# 	last_name=last_name
			# 		)
			# u.set_password(password)
			# u.save()

			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('profile')

	# if the request method is GET type
	form = RegisterForm()
	return render(request, 'accounts/register.html', {'form': form})

