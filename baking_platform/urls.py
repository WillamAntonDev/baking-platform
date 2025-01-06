from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from recipes.views import home_page  # Import the home_page view

urlpatterns = [
    path('', home_page, name='home'),  # Map the home_page view to the root URL
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),  # Include app-specific URLs
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
