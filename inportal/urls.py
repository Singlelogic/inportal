from django.contrib import admin
from django.urls import path, include

from .views import main_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    path('dct/', include('dct.urls')),
    path('client/', include('client.urls')),
    path('', main_page, name='main_page'),
]
