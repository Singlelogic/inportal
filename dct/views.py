from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import DataCollectTerminalForm
from .models import (
    DataCollectTerminal, Accumulator, AccumulatorDate
)


class DataCollectTerminalListView(ListView):
    """Output a list of data collection terminals."""
    model = DataCollectTerminal


class DataCollectTerminalUpdate(UpdateView):
    """Update the selected data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_update.html'
    fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
              'accumulator', 'remark']
    success_url = reverse_lazy('list_dct_url')

    def form_valid(self, form):
        """
        Called to change the state of the battery.
        Possible states:
        1. Installed
        2. Uninstalled
        """
        accum_in_db = DataCollectTerminal.objects.get(id=self.object.id).accumulator
        accum_in_form = self.object.accumulator
        if accum_in_db != accum_in_form:
            if accum_in_db:
                accum_in_db.changed_status(2)
            else:
                accum_in_form.changed_status(1)
        return super().form_valid(form)


class DataCollectTerminalCreateView(CreateView):
    """Create data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_create.html'
    # fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
    #           'accumulator', 'remark']
    form_class = DataCollectTerminalForm
    success_url = reverse_lazy('list_dct_url')

    # def get_context_data(self, **kwargs):
    #     super().get_context_data()
    #     print(self.kwargs['accumulator_id'])


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
