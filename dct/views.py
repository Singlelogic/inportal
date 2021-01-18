from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import DataCollectTerminal


def index(request):
    dcts = DataCollectTerminal.objects.all()
    context = {'dcts': dcts}
    return render(request, 'dct/index.html', context)


class DataCollectTerminalDetail(DetailView):
    model = DataCollectTerminal
