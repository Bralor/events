from django.contrib import admin
from django.urls import path, include

urlpatterns = 	[
    path('', include('explorea.events.urls')),
    path('accounts/', include('explorea.accounts.urls')),
    path('admin/', admin.site.urls),
				]
