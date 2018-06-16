from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/events/'}, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', auth_views.password_reset, 
        {'template_name': 'accounts/reset_password.html', 
        'post_reset_redirect':'password_reset_done',
        'email_template_name':'accounts/reset_password_email.html'}, name='reset_password'),
    path('reset-password/done/', auth_views.password_reset_done,  name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, 
        {'post_reset_redirect':'password_reset_complete'}, name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.password_reset_complete, name='password_reset_complete'),

]