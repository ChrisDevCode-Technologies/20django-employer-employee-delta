from django.shortcuts import render

def home_view(request):
    """
    Render the home page.
    """
    return render(request, 'base.html')
