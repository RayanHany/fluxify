from django.shortcuts import render,redirect
from .models import post_mark

# Create your views here.
def list(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    return render(request, 'listing-page.html')
