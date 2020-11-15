from django.shortcuts import render


def index(request):
    """
    Main template rendering
    """
    return render(request, 'frontend/index.html')
