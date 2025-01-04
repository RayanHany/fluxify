from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home-page.html')

def settings(request):
    return render(request, 'settings-page.html')

def chat(request):
    return render(request, 'chat-page.html')


def profile(request):
    return render(request, 'profile-page.html')



