from django.conf import settings
from django.contrib import admin
from explorea.events import views
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = 	[
	path('', views.index, name='index'),
	path('events/', include('explorea.events.urls', namespace='events')),
    path('accounts/', include('explorea.accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path('cart/', include('explorea.cart.urls', namespace='cart')),
				]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)