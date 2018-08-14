from . import views
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
										password_reset,
										password_reset_done,
										password_reset_confirm,
										password_reset_complete
										)

app_name = 'accounts'

urlpatterns = 	[
	path('login/', auth_views.login,{'template_name': 'accounts/login.html'}, name='login'),
	path('logout/', auth_views.logout,{'template_name': 'accounts/logged_out.html'}, name='logout'),
	path('register/', views.register, name='register'),
	path('profile/', views.profile, name='profile'),

	path('hosts/', views.host_list, name='host_list'),
	path('become-host/', views.become_host, name='become_host'),
	path('host/profile/<username>/', views.host_profile, name='host_profile'),

	path('profile/edit/', views.edit_profile, name='edit_profile'),
	path('change-password/', views.change_password, name='change_password'),
	path('reset_password/complete', password_reset_complete, name='password_reset_complete'),
	path('reset-password/done/', password_reset_done, name='password_reset_done'),
	path('reset-password/', password_reset,{'template_name': 'accounts/reset_password.html',
		'post_reset_redirect': 'password_reset_done',
		'email_template_name': 'accounts/reset_password_email.html'},
		name='reset_password'),

	url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
		{'post_reset_redirect': 'password_reset_complete'}, name='password_reset_confirm'),
	url(r'^become-host/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.activate_host, 
		name='activate_host'),
				]