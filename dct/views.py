from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import DataCollectTerminalForm
from .mixins import ModifiedMethodFormValidMixim
from .models import DataCollectTerminal, Accumulator


class DataCollectTerminalCreateView(ModifiedMethodFormValidMixim, CreateView):
    """Create data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_create.html'
    form_class = DataCollectTerminalForm
    success_url = reverse_lazy('list_dct_url')


class DataCollectTerminalListView(ListView):
    """Output a list of data collection terminals."""
    model = DataCollectTerminal


class DataCollectTerminalUpdate(ModifiedMethodFormValidMixim, UpdateView):
    """Update the selected data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_update.html'
    fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
              'accumulator', 'remark']
    success_url = reverse_lazy('list_dct_url')


class DataCollectTerminalDeleteView(DeleteView):
    """Delete data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_delete.html'
    success_url = reverse_lazy('list_dct_url')


class AccumulatorCreateView(CreateView):
    """Create accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_create.html'
    fields = ['number', 'remark']
    success_url = reverse_lazy('list_accumulator_url')


class AccumulatorListView(ListView):
    """Output a list of accumulators."""
    model = Accumulator


class AccumulatorUpdateView(UpdateView):
    """Update the selected accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_update.html'
    fields = ['number', 'remark']
    success_url = reverse_lazy('list_accumulator_url')


class AccumulatorDeleteView(DeleteView):
    """Delete accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_delete.html'
    success_url = reverse_lazy('list_accumulator_url')
