from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Client


class ClientCreateView(CreateView):
    """Create client."""
    model = Client
    template_name = 'client/client_create.html'
    fields = ['client']
    success_url = reverse_lazy('list_client_url')


class ClientListView(ListView):
    """List of clients."""
    model = Client


class ClientUpdateView(UpdateView):
    """Update the selected client."""
    model = Client
    template_name = 'client/client_update.html'
    fields = ['client']
    success_url = reverse_lazy('list_client_url')


class ClientDeleteView(DeleteView):
    """Delete the selected client."""
    model = Client
    template_name = 'client/client_delete.html'
    success_url = reverse_lazy('list_client_url')
