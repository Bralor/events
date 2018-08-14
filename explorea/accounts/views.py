# imports lower are important in the "become_host" view 
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# aaa
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
# a
from .models import Profile
# b
from .forms import RegisterForm, EditProfileForm, EditUserForm


token_generator = PasswordResetTokenGenerator()
UserModel = get_user_model()


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
	''' we want to edit our profile section '''
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


@login_required
def host_list(request):
	''' This view is accessible only to those registerred at our site.'''
	profiles = Profile.objects.filter(is_host=True)
	if request.user.profile.is_host:
		profiles = profiles.exclude(user__pk=request.user.id)

	return render(request, 'accounts/host_list.html', {'profiles':profiles})


@login_required
def become_host(request):
	''' aaa '''
	verificationEmailTemplate = 'accounts/hostVerificationEmail.html'
	emailContext = {
		'user': request.user,
		'domain': get_current_site(request).domain,
		'uidb64': urlsafe_base64_encode(force_bytes(request.user.pk)).decode(),
		'token': token_generator.make_token(request.user)
					}
	html_body 	= render_to_string(verificationEmailTemplate, emailContext)
	subject 	= 'Explorea Host Verification'
	from_email 	= 'admin@explorea.com'
	to_email 	= request.user.email
	email 		= EmailMessage(subject, html_body, from_email, [to_email])
	email.send()

	return render(request, 'accounts/verificationSent.html')


def activate_host(request, uidb64, token):
	'''We want to render html correctly with proper urls.'''
	try:
		uid 	= urlsafe_base64_decode(uidb64).decode()
		user 	= UserModel._default_manager.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user 	= None

	if user is not None and token_generator.check_token(user, token):
		user.profile.is_host = True
		user.profile.save()
		return render(request, 'accounts/verificationComplete.html')
	else:
		return render(request, 'accounts/invalidLink.html')


@login_required
def host_profile(request, username):
    host = UserModel.objects.get(username=username)
    return render(request, 'accounts/hostProfile.html', {'host': host})