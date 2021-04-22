from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import DCTForm
from .mixins import ModifiedMethodFormValidMixim, SuccessURLAccumMixin
from .models import DataCollectTerminal, Accumulator
from .utils import add_order_filter_context


class DataCollectTerminalCreateView(LoginRequiredMixin, ModifiedMethodFormValidMixim, CreateView):
    """Create data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_create.html'
    form_class = DCTForm
    success_url = reverse_lazy('list_dct_url')

    def get_form(self, form_class=DCTForm, **kwargs):
        """
        Excluded from the drop-down list of decommissioned batteries,
        batteries linked to other terminals.
        Excludes from the list of users to which the terminal is already linked.
        """
        form = super().get_form(**kwargs)
        qs = DataCollectTerminal.get_special_queryset()
        form.fields['accumulator'].queryset = qs.get('qs_accum')
        form.fields['user'].queryset = qs.get('qs_user')
        return form


class DataCollectTerminalListView(LoginRequiredMixin, ListView):
    """Output a list of data collection terminals."""
    model = DataCollectTerminal

    def get_context_data(self, **kwargs):
        """
        Adds sorted data by user, battery number, or truncated name field
        number to the context.
        Adds the value by which the sorting was performed to the context.
        """
        context = super().get_context_data(**kwargs)
        order = self.request.GET.get('order', '')
        context['order'] = order
        context['datacollectterminal_list'] = DataCollectTerminal.order(order)
        return context


class DataCollectTerminalUpdate(LoginRequiredMixin, ModifiedMethodFormValidMixim, UpdateView):
    """Update the selected data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_update.html'
    form_class = DCTForm

    def get_context_data(self, **kwargs):
        """Adding a sortation order to the context."""
        context = super().get_context_data(**kwargs)
        context['order'] = self.request.GET.get('order', '')
        return context

    def get_success_url(self):
        """
        Redirects to a page with the sorting that was set when you went
        to this page.
        """
        order = self.request.GET.get('order', '')
        return f"{reverse_lazy('list_dct_url')}?order={order}"

    def get_form(self, form_class=DCTForm, **kwargs):
        """
        Excluded from the drop-down list of decommissioned batteries,
        batteries linked to other terminals.
        Excludes from the list of users to which the terminal is already linked.
        """
        form = super().get_form(**kwargs)
        qs = DataCollectTerminal.get_special_queryset(self.object, self.object.user)
        form.fields['accumulator'].queryset = qs.get('qs_accum')
        form.fields['user'].queryset = qs.get('qs_user')
        return form


class DataCollectTerminalDeleteView(LoginRequiredMixin, DeleteView):
    """Delete data collection terminal."""
    model = DataCollectTerminal
    template_name = 'dct/datacollectterminal_delete.html'

    def delete(self, request, *args, **kwargs):
        """
        Changing the status of the battery to extracted when deleting
        the terminal.
        """
        object = self.get_object()
        if object.accumulator:
            object.accumulator.changed_status(2)
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Adding a sortation order to the context."""
        context = super().get_context_data(**kwargs)
        context['order'] = self.request.GET.get('order', '')
        return context

    def get_success_url(self):
        """
        Redirects to a page with the sorting that was set when you
        went to this page.
        """
        order = self.request.GET.get('order', '')
        return f"{reverse_lazy('list_dct_url')}?order={order}"


class AccumulatorCreateView(LoginRequiredMixin, SuccessURLAccumMixin, CreateView):
    """Create accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_create.html'
    fields = ['number', 'debited', 'remark']

    def get_context_data(self, **kwargs):
        """Adding sorting and filtering data to the context."""
        context = super().get_context_data(**kwargs)
        context.update(add_order_filter_context(self.request))
        return context


class AccumulatorListView(LoginRequiredMixin, ListView):
    """Output a list of accumulators."""
    model = Accumulator

    def get_context_data(self, **kwargs):
        """Adding sorting and filtering data to the context."""
        context = super().get_context_data(**kwargs)
        filtering = self.request.GET.get('filtering', '')
        context['filtering'] = filtering
        order = self.request.GET.get('order', '')
        context['order'] = order
        qs = Accumulator.get_special_queryset(order=order, filtering=filtering)
        context['accumulator_list'] = qs
        return context


class AccumulatorUpdateView(LoginRequiredMixin, SuccessURLAccumMixin, UpdateView):
    """Update the selected accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_update.html'
    fields = ['number', 'debited', 'remark']

    def get_context_data(self, **kwargs):
        """Adding sorting and filtering data to the context."""
        context = super().get_context_data(**kwargs)
        context.update(add_order_filter_context(self.request))
        return context


class AccumulatorDeleteView(LoginRequiredMixin, SuccessURLAccumMixin, DeleteView):
    """Delete accumulator."""
    model = Accumulator
    template_name = 'dct/accumulator_delete.html'

    def get_context_data(self, **kwargs):
        """Adding sorting and filtering data to the context."""
        context = super().get_context_data(**kwargs)
        context.update(add_order_filter_context(self.request))
        return context


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
