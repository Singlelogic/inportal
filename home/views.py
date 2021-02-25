from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Returns the main page."""
    return render(request, 'home/index.html')
