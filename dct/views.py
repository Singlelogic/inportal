from textwrap import dedent

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import DataCollectTerminalForm
from .mixins import ModifiedMethodFormValidMixim
from .models import DataCollectTerminal, Accumulator


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
        Sort objects by user, battery number, or truncated name field number.
        """
        context = super().get_context_data(**kwargs)
        context['order'] = self.request.GET.get('order', '')

        if context['order'] == '-number':
            context['datacollectterminal_list'] = sorted(DataCollectTerminal.objects.all(),
                                                         reverse=True)
        elif context['order'] == 'user':
            context['datacollectterminal_list'] = DataCollectTerminal.objects.order_by('user')
        elif context['order'] == '-user':
                context['datacollectterminal_list'] = DataCollectTerminal.objects.raw(
                    dedent('''\
                        SELECT *
                        FROM dct_datacollectterminal
                        LEFT JOIN client_client ON user_id=client_client.id
                        ORDER BY client_client.client DESC NULLS LAST;'''))
        elif context['order'] == 'accum':
            context['datacollectterminal_list'] = \
                DataCollectTerminal.objects.order_by('accumulator')
        elif context['order'] == '-accum':
            context['datacollectterminal_list'] = DataCollectTerminal.objects.raw(
                dedent('''\
                    SELECT *
                    FROM dct_datacollectterminal
                    ORDER BY accumulator_id DESC NULLS LAST;'''))
        else:
            context['datacollectterminal_list'] = sorted(DataCollectTerminal.objects.all())
        return context


class DataCollectTerminalUpdate(LoginRequiredMixin, ModifiedMethodFormValidMixim, UpdateView):
    """Update the selected data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_update.html'
    fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
              'accumulator', 'remark']
    success_url = reverse_lazy('list_dct_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.request.GET.get('order', '')
        return context


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


class AccumulatorDeleteView(LoginRequiredMixin, DeleteView):
    """Delete accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_delete.html'
    success_url = reverse_lazy('list_accumulator_url')


class EquipmentListView(LoginRequiredMixin, TemplateView):
    """Equipment List"""
    template_name = 'dct/equipment_list.html'


class DCTRemarkListView(LoginRequiredMixin, TemplateView):
    """List of terminal notes."""
    template_name = 'dct/dctremark_list.html'

    def get_context_data(self, **kwargs):
        """Adding a list of notes for a specific terminal to the context."""
        context = super().get_context_data(**kwargs)
        dct = get_object_or_404(DataCollectTerminal, slug=context['slug'])
        context['dctremarks'] = dct.datacollectterminalremark_set.all()
        return context
