from django.shortcuts import render


def main_page(request):
    """Returns the main blank page."""
    return render(request, 'main_page.html')
