from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import DataCollectTerminalForm
from .mixins import ChangedStatusAccum
from .models import (
    DataCollectTerminal, Accumulator, AccumulatorDate
)


class DataCollectTerminalListView(ListView):
    """Output a list of data collection terminals."""
    model = DataCollectTerminal


class DataCollectTerminalUpdate(ChangedStatusAccum, UpdateView):
    """Update the selected data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_update.html'
    fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
              'accumulator', 'remark']
    success_url = reverse_lazy('list_dct_url')


class DataCollectTerminalCreateView(ChangedStatusAccum, CreateView):
    """Create data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_create.html'
    # fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
    #           'accumulator', 'remark']
    form_class = DataCollectTerminalForm
    success_url = reverse_lazy('list_dct_url')


class AccumulatorListView(ListView):
    """Output a list of accumulators."""
    model = Accumulator


class AccumulatorCreateView(CreateView):
    """Create accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_create.html'
    fields = ['number', 'remark']
    success_url = reverse_lazy('list_accumulator_url')


class AccumulatorUpdateView(UpdateView):
    """Update the selected accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_update.html'
    fields = ['number', 'remark']
    success_url = reverse_lazy('list_accumulator_url')
