from django.shortcuts import render
from .models import post_mark

# Create your views here.
def list(request):
    return render(request, 'listing-page.html')
