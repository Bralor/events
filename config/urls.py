from django.contrib import admin
from django.urls import path, include

urlpatterns = 	[
    path('', include('explorea.events.urls', namespace='events')),
    path('accounts/', include('explorea.accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
				]
