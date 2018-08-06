from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, EditProfileForm, EditUserForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
	''' This function render only basic information about the user's account '''

	return render(request, 'accounts/profile.html')


def register(request):
	''' The register function. '''

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


@login_required
def edit_profile(request):
	
    UserForm = EditUserForm(request.POST or None, instance=request.user)
    ProfileForm = EditProfileForm(request.POST or None, request.FILES or None,
        instance=request.user.profile)

    if request.method == 'POST':

        if UserForm.is_valid() and ProfileForm.is_valid():
            user = UserForm.save()
            profile = ProfileForm.save()
            
            return redirect('accounts:profile')

    return render(request, 'accounts/edit_profile.html', 
        {'UserForm': UserForm, 'ProfileForm': ProfileForm})


@login_required
def change_password(request):
	''' The user wants to change his current password'''

	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		
		if form.is_valid():
			user = form.save()
			# we need to obtain a new session hash due to new password
			update_session_auth_hash(request, user)
			return redirect('accounts/profile/')
		else:
			return render(request, 'accounts/change_password.html', {'form': form})
	
	# GET method
	else:
		form = PasswordChangeForm(user=request.user)
		return render(request, 'accounts/change_password.html', {'form': form})

