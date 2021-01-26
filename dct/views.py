from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import DataCollectTerminal


class DataCollectTerminalListView(ListView):
    """Output a list of data collection terminals."""
    queryset = DataCollectTerminal.objects.all()


class DataCollectTerminalDetail(DetailView):
    """Detailed output of the selected data collection terminal."""
    model = DataCollectTerminal
