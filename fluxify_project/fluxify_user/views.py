from django.shortcuts import render,redirect
from django.contrib import messages
from fluxify_user.models import user_custome
from django.http import HttpResponse



# Create your views here.
def home(request):
    return render(request, 'home-page.html')

def settings(request):
    return render(request, 'settings-page.html')

def chat(request):
    return render(request, 'chat-page.html')


def profile(request):
    return render(request, 'profile-page.html')

def login(request):
    return render(request, 'login-page.html')



def signup(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        mail_id = request.POST.get("mail_id")
        password = request.POST.get("password")
        phone_no = request.POST.get("phone_no")
        pin_code = request.POST.get("pin_code")
        address = request.POST.get("address")
        profile_photo = request.FILES.get("profile_photo")

        # Save to the database (example model)
        user_custome.objects.create(
            user_name=user_name,
            mail_id=mail_id,
            password=password,
            phone_no=phone_no,
            pin_code=pin_code,
            address=address,
            profile_photo=profile_photo,
        )
        return HttpResponse("Home-page.html")
    return render(request, "signup-page.html")




