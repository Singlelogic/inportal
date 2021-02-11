from django.urls import path


from .views import (
    ClientListView, ClientCreateView, ClientUpdateView
)


urlpatterns = [
    path('list_user/', ClientListView.as_view(), name='list_user_url'),
    path('create_user/', ClientCreateView.as_view(), name='create_user_url'),
    path('update_user/<int:pk>/', ClientUpdateView.as_view(), name='update_client_url'),
]
