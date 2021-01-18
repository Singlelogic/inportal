from django.urls import path

from .views import index, DataCollectTerminalDetail


urlpatterns = [
    path('', index, name='index'),
    path('detail_dct/<int:pk>/', DataCollectTerminalDetail.as_view(), name='detail_dct'),
]