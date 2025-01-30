from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from fluxify_user.models import user_custome,SavedPost,report,help
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


def save_post(request, post_id):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')

    # Retrieve the user and post
    user_email = request.session.get('mail_id')
    user = user_custome.objects.filter(mail_id=user_email).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect('login_page')

    try:
        post = post_mark.objects.get(id=post_id)
        # Check if the post is already saved
        if SavedPost.objects.filter(user=user, post=post).exists():
            messages.info(request, "Post already saved.")
        else:
            SavedPost.objects.create(user=user, post=post)
            messages.success(request, "Post saved successfully.")
    except post_mark.DoesNotExist:
        messages.error(request, "Post does not exist.")
    
    return redirect('post_details',id=post_id)  # Replace with your profile page URL name


def profile_page_saved(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    
    user_email = request.session.get('mail_id')
    user = user_custome.objects.filter(mail_id=user_email).first()
    
    saved_posts = SavedPost.objects.filter(user=user).select_related('post')

    context = {
        'user': user,
        'saved_posts': saved_posts,
    }
    return render(request, 'profile-page-saved.html', context)

def report_issue(request):
    try:
        if not request.session.get('is_logged_in'):
            return redirect('login_page')

        user_email = request.session.get('mail_id')
        user = user_custome.objects.filter(mail_id=user_email).first()

        if not user:
            messages.error(request, "User not found.")
            return redirect('login_page')

        if request.method == 'POST':
            post_image = request.FILES.get('post_image')
            post_description = request.POST.get('post_description', '')

            if not post_image:
                messages.error(request, "Please upload an image.")
                return redirect('report_issue')

            # Save the report
            report.objects.create(
                user=user,
                report_image=post_image,
                report_text=post_description
            )
            messages.success(request, "You have a New Report to Check.")
            return redirect('home_page')  # Redirect after successful submission

    except Exception as e:
        messages.error(request, "Something went wrong. Please try again.")
        print("Error:", e)  # Logs the actual error for debugging

    return render(request, 'report.html')


def submit_help_request(request):
    try:
        if not request.session.get('is_logged_in'):
            return redirect('login_page')

        user_email = request.session.get('mail_id')
        user = user_custome.objects.filter(mail_id=user_email).first()

        if not user:
            messages.error(request, "User not found.")
            return redirect('login_page')

        if request.method == 'POST':
            help_image = request.FILES.get('help_image')
            help_description = request.POST.get('help_description', '')

            if not help_image:
                messages.error(request, "Please upload an image.")
                return redirect('submit_help_request')

            # Save the help request
            help.objects.create(
                user=user,
                help_image=help_image,
                help_text=help_description
            )
            messages.success(request, "You Have A New Help Message To Check.")
            return redirect('home_page')  # Redirect after successful submission

    except Exception as e:
        messages.error(request, "Something went wrong. Please try again.")
        print("Error:", e)  # Logs the actual error for debugging

    return render(request, 'help.html')