from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Client


class ClientListView(ListView):
    """List of clients."""
    model = Client


class ClientUpdateView(UpdateView):
    """Update the selected data collection terminal."""
    model = Client
    template_name = 'client/client_update.html'
    fields = ['client']
    success_url = reverse_lazy('list_user_url')


class ClientCreateView(CreateView):
    """Create data collection terminal."""
    model = Client
    template_name = 'client/client_create.html'
    fields = ['client']
    success_url = reverse_lazy('list_user_url')
