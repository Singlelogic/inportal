from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('account.urls')),
    path('dct/', include('dct.urls')),
    path('client/', include('client.urls')),
    path('blog/', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),
]

"""############################################ FOR BLOG ############################################"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""########################################## END FOR BLOG ##########################################"""