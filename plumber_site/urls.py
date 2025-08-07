from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('quotes/', include('quotes.urls')),
    path('portal/', include('customers.urls')),
    path('', include('main.urls')),
    path('', include('areas.urls')),
]

# Add production URLs
if not settings.DEBUG:
    urlpatterns.insert(-2, path('monitoring/', include('monitoring.urls')))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)