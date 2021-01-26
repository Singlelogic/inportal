from django.urls import path

from .views import DataCollectTerminalDetail, DataCollectTerminalListView


urlpatterns = [
    path('', DataCollectTerminalListView.as_view(), name='list_dct_url'),
    path('detail_dct/<int:pk>/', DataCollectTerminalDetail.as_view(), name='detail_dct'),
]