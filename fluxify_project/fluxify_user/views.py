from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from fluxify_user.models import user_custome
from django.contrib.auth.hashers import check_password, make_password
from fluxify_post.models import post_mark
from functools import wraps

# Home page view
def home(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    
    # Retrieve the email from the session
    user_email=request.session.get('mail_id')
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first() 
    
    post = post_mark.objects.all().order_by('?')  # Random order
    
    return render(request, 'Home-page.html', {'post': post, 'user': user})
        
# Settings page view
def settings(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    
    # Retrieve the email from the session
    user_email=request.session.get('mail_id')
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first() 


    return render(request, 'settings-page.html', {'user': user})


# Profile page view
def profile(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    
    # Retrieve the email from the session
    user_email=request.session.get('mail_id')
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first() 

     # Get all posts created by the logged-in user
    user_posts = post_mark.objects.filter(posted_by=user)
    
    return render(request, 'profile-page.html', {'user': user,'user_posts':user_posts})

# Login page view
def login(request):
    if request.method == 'POST' and 'login' in request.POST:
        mail_id = request.POST.get("mail_id")  # Email field
        password = request.POST.get("password")  # Password field
        
        try:
            user = user_custome.objects.get(mail_id=mail_id)  # Find user by email
            if check_password(password, user.password):  # Validate password
                request.session['is_logged_in'] = True
                request.session['mail_id'] = mail_id
                return redirect('home_page')  # Redirect to home page
            else:
                 error_message = "Invalid Password Please Try Again"
                 messages.error(request, error_message)
            return redirect('login_page')
        except user_custome.DoesNotExist:
                messages.error(request, "Account does not exist. Please sign up to continue.")
                return redirect('signup_page')
    return render(request, "login-page.html")



# Signup page view
def signup(request):
    if request.method == 'POST' and 'register' in request.POST:
        try:  
            user_name = request.POST.get("user_name")
            mail_id = request.POST.get("mail_id")
            password = request.POST.get("password")
            phone_no = request.POST.get("phone_no")
            pin_code = request.POST.get("pin_code")
            address = request.POST.get("address")
            profile_photo = request.FILES.get("profile_photo")

            # Check if the email or phone number already exists
            if user_custome.objects.filter(mail_id=mail_id).exists():
                messages.error(request, "Email is already registered.")
                return redirect('signup_page')

            if user_custome.objects.filter(phone_no=phone_no).exists():
                messages.error(request, "Phone number is already registered.")
                return redirect('signup_page')

            # Hash the password before saving
            hashed_password = make_password(password)

            # Save user to the database
            user_custome.objects.create(
                user_name=user_name,
                mail_id=mail_id,
                password=hashed_password,
                phone_no=phone_no,
                pin_code=pin_code,
                address=address,
                profile_photo=profile_photo,
            )
            request.session['is_logged_in'] = True
            request.session['mail_id'] = mail_id 
            return redirect('home_page')
        except Exception as e:
            error_message = "Error occurred. Please try again."
            messages.error(request, error_message)
            return redirect('signup_page')
            
    return render(request, "signup-page.html")



def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if the user is logged in based on session
        if not request.session.get('is_logged_in', False):
            return redirect('login_page')  # Redirect to login page if not logged in
        return view_func(request, *args, **kwargs)
    return wrapper



def user_logout(request):
    if request.session.get('is_logged_in'):
        # Clear session data
        request.session.flush()  # Removes all session data
        messages.success(request, 'You have successfully logged out.')

    return redirect('login_page')


def user_b(request,id):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    
    # Get the user object by ID
    user=user_custome.objects.get(id=id)

    # Fetch posts of the given user using the related_name 'posts'
    posts = user.posts.all()

     # Pass both the user and posts to the template context
    context = {'user': user, 'posts': posts}
    

    
    return render(request, "user-b-profile-page.html",context)    