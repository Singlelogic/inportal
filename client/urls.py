from django.urls import path


from .views import (
    ClientDeleteView, ClientCreateView, ClientListView, ClientUpdateView
)


urlpatterns = [
    path('create_user/', ClientCreateView.as_view(), name='create_client_url'),
    path('list_user/', ClientListView.as_view(), name='list_client_url'),
    path('update_user/<int:pk>/', ClientUpdateView.as_view(), name='update_client_url'),
    path('delete_user/<int:pk>/', ClientDeleteView.as_view(), name='delete_client_url'),
]
