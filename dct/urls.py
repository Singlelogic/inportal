from django.urls import path

from .views import (
    AccumulatorCreateView, AccumulatorListView, AccumulatorUpdateView,
    DataCollectTerminalListView, DataCollectTerminalCreateView, DataCollectTerminalUpdate,
)


urlpatterns = [
    path('create_dct/', DataCollectTerminalCreateView.as_view(), name='create_dct_url'),
    path('update_dct/<int:pk>/', DataCollectTerminalUpdate.as_view(), name='update_dct_url'),
    path('list_dct', DataCollectTerminalListView.as_view(), name='list_dct_url'),

    path('create_accumulator/', AccumulatorCreateView.as_view(), name='create_accumulator_url'),
    path('list_accumulator', AccumulatorListView.as_view(), name='list_accumulator_url'),
    path('update_accumulator/<int:pk>/', AccumulatorUpdateView.as_view(), name='update_accumulator_url'),
]