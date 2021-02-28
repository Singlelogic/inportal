from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import DataCollectTerminalForm
from .mixins import ModifiedMethodFormValidMixim
from .models import DataCollectTerminal, Accumulator
from .utils import accum_lifetime


class DataCollectTerminalCreateView(LoginRequiredMixin, ModifiedMethodFormValidMixim, CreateView):
    """Create data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_create.html'
    form_class = DataCollectTerminalForm
    success_url = reverse_lazy('list_dct_url')


class DataCollectTerminalListView(LoginRequiredMixin, ListView):
    """Output a list of data collection terminals."""
    model = DataCollectTerminal

    def get_context_data(self, **kwargs):
        """
        Temporarily. Rewrite!!!
        Sorting objects by the truncated number of the name field.
        """
        context = super().get_context_data(**kwargs)
        context['datacollectterminal_list'] = sorted(DataCollectTerminal.objects.all())
        return context


class DataCollectTerminalUpdate(LoginRequiredMixin, ModifiedMethodFormValidMixim, UpdateView):
    """Update the selected data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_update.html'
    fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
              'accumulator', 'remark']
    success_url = reverse_lazy('list_dct_url')


class DataCollectTerminalDeleteView(LoginRequiredMixin, DeleteView):
    """Delete data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_delete.html'
    success_url = reverse_lazy('list_dct_url')

    def delete(self, request, *args, **kwargs):
        """
        Changing the status of the battery to extracted when
        deleting the terminal.
        """
        object = self.get_object()
        if object.accumulator:
            object.accumulator.changed_status(2)
        return super().delete(request, *args, **kwargs)


class AccumulatorCreateView(LoginRequiredMixin, CreateView):
    """Create accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_create.html'
    fields = ['number', 'remark']
    success_url = reverse_lazy('list_accumulator_url')


class AccumulatorListView(LoginRequiredMixin, ListView):
    """Output a list of accumulators."""
    model = Accumulator


class AccumulatorUpdateView(LoginRequiredMixin, UpdateView):
    """Update the selected accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_update.html'
    fields = ['number', 'remark']
    success_url = reverse_lazy('list_accumulator_url')

    def get_context_data(self, **kwargs):
        """Adding the number of days used by the battery to the form."""
        context = super().get_context_data(**kwargs)
        context['lifetime'] = accum_lifetime(context['object'])
        return context


class AccumulatorDeleteView(LoginRequiredMixin, DeleteView):
    """Delete accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_delete.html'
    success_url = reverse_lazy('list_accumulator_url')


class EquipmentListView(LoginRequiredMixin, TemplateView):
    """Equipment List"""
    template_name = 'dct/equipment_list.html'
