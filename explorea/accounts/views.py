from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm

def profile(request):
	return render(request, 'accounts/profile.html')


def register(request):
	if request.method == 'POST':
		# Create thte form and populate it with data from the POST request
		form = RegisterForm(request.POST)

		# Validate the data in the form
		if form.is_valid():
			user = form.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('profile')

	# if the request method is GET type
	form = RegisterForm()
	return render(request, 'accounts/register.html', {'form': form})


def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)

		if form.is_valid():
			user = form.save()
			request.session['profile_changes'] = request.session.setdefault('profile_changes', 0) + 1
			return redirect('profile')

	form = EditProfileForm(instance=request.user)
	return render(request, 'accounts/edit_profile.html', {'form': form})


def change_password(request):
	''' The user wants to change his current password'''
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			user = form.save()
			# we need to obtain a new session hash due to new password
			update_session_auth_hash(request, user)
			return redirect('accounts/profile/')
	
	# GET method
	else:
		form = PasswordChangeForm(user=request.user)
		return render(request, 'accounts/change_password.html', {'form': form})

