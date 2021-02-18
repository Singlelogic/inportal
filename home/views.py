from django.shortcuts import render


def index(request):
    """Returns the main page."""
    return render(request, 'home/index.html')
