from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from fluxify_user.models import user_custome,SavedPost,report,help, verification
from django.contrib.auth.hashers import check_password, make_password
from fluxify_post.models import post_mark
from functools import wraps
import random
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from .models import user_custome, OTPVerification

# Home page view
def home(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    
    # Retrieve the email from the session
    user_email=request.session.get('mail_id')

    
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first()

    try:
            verification_record = verification.objects.get(user=user)
            
            # If verified, update the user role to 'influencer'
            if verification_record.verifyed:
                user.user_role = 'influencer'
                user.save()  # Save the updated role

            else:
                user.user_role = 'advertiser'
                user.save()    
                
    except verification.DoesNotExist:
         pass  # If no verification record exists, nothing changes
    
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

    try:
            verification_record = verification.objects.get(user=user)
            
            # If verified, update the user role to 'influencer'
            if verification_record.verifyed:
                user.user_role = 'influencer'
                user.save()  # Save the updated role

            else:
                user.user_role = 'advertiser'
                user.save()    
                
    except verification.DoesNotExist:
         pass  # If no verification record exists, nothing changes


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

    try:
            verification_record = verification.objects.get(user=user)
            
            # If verified, update the user role to 'influencer'
            if verification_record.verifyed:
                user.user_role = 'influencer'
                user.save()  # Save the updated role

            else:
                user.user_role = 'advertiser'
                user.save()    
                
    except verification.DoesNotExist:
         pass  # If no verification record exists, nothing changes
    
    return render(request, 'profile-page.html', {'user': user,'user_posts':user_posts})

# Login page view
def login(request):
    if request.session.get('is_logged_in'):
            return redirect('home_page')  # Redirect to home page if already logged in
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


# send otp view
def send_otp_email(mail_id, otp_code):
    """Function to send OTP to email"""
    subject = "Your OTP for Account Verification"
    message = (
        "Dear User,\n\n"
        "Your One-Time Password (OTP) for account verification is:\n\n"
        f"🔒 **{otp_code}** 🔒\n\n"
        "This OTP is valid for **5 minutes**. Do not share it with anyone.\n\n"
        "If you did not request this, please ignore this email.\n\n"
        "Best regards,\n"
        "Flexify Team"
    )
    sender_email = "fluxify.inc@gmail.com"  #  sender email
    try:
        send_mail(subject, message, sender_email, [mail_id])
    except BadHeaderError:
        print("Invalid header found.")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")  # Debugging print

# Signup page view
def signup(request):
    if request.method == 'POST' and 'register' in request.POST:
        if request.session.get('is_logged_in'):
            return redirect('home_page')  # Redirect to home page if already logged in
        try:
            user_name = request.POST.get("user_name")
            mail_id = request.POST.get("mail_id")
            password = request.POST.get("password")
            phone_no = request.POST.get("phone_no")
            pin_code = request.POST.get("pin_code")
            address = request.POST.get("address")
            profile_photo = request.FILES.get("profile_photo")

            # Check if email or phone already exists
            if user_custome.objects.filter(mail_id=mail_id).exists():
                messages.error(request, "Email is already registered.")
                return redirect('signup_page')

            if user_custome.objects.filter(phone_no=phone_no).exists():
                messages.error(request, "Phone number is already registered.")
                return redirect('signup_page')

            # Hash the password before storing it
            hashed_password = make_password(password)

            # Save user data in session before final registration
            request.session['signup_data'] = {
                'user_name': user_name,
                'mail_id': mail_id,
                'password': hashed_password,
                'phone_no': phone_no,
                'pin_code': pin_code,
                'address': address,
                'profile_photo': profile_photo.name if profile_photo else None,
            }

            # Get or create the user instance
            user_instance, created = user_custome.objects.get_or_create(
                mail_id=mail_id,
                defaults={'user_name': user_name, 'phone_no': phone_no, 'password': hashed_password, 'pin_code': pin_code, 'address': address, 'profile_photo': profile_photo}
            )

            # Generate OTP
            otp_code = str(random.randint(100000, 999999))

            # Save OTP linked to the user
            otp_entry, created = OTPVerification.objects.update_or_create(
                user=user_instance,
                defaults={'otp_code': otp_code}
            )

            # Send OTP to email
            send_otp_email(mail_id, otp_code)

            messages.success(request, "OTP sent to your email. Please verify.")
            return redirect('verify_otp')

        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")  # Print actual error message
        return redirect('signup_page')

    return render(request, "signup-page.html")

#verify otp view
def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        mail_id = request.session.get('signup_data', {}).get('mail_id')

        if not mail_id:
            messages.error(request, "Session expired. Please sign up again.")
            return redirect('signup_page')

        try:
            # Fetch the saved user instance instead of creating a new one
            user_instance = user_custome.objects.get(mail_id=mail_id)

            # Fetch the OTP record linked to the saved user
            otp_record = OTPVerification.objects.get(user=user_instance, otp_code=otp_code)

            if otp_record.is_valid():
                # Save user details permanently
                signup_data = request.session.pop('signup_data', {})
                user_instance.user_name = signup_data['user_name']
                user_instance.password = signup_data['password']
                user_instance.phone_no = signup_data['phone_no']
                user_instance.pin_code = signup_data['pin_code']
                user_instance.address = signup_data['address']
                if signup_data.get('profile_photo'):
                    user_instance.profile_photo = signup_data['profile_photo']

                user_instance.save()  # Save the user instance

                # Delete OTP record after successful verification
                otp_record.delete()

                # Log in the user
                request.session['is_logged_in'] = True
                request.session['mail_id'] = mail_id
                return redirect('home_page')

            else:
                messages.error(request, "OTP expired. Please sign up again.")
                return redirect('signup_page')

        except user_custome.DoesNotExist:
            messages.error(request, "User not found. Please sign up again.")
            return redirect('signup_page')

        except OTPVerification.DoesNotExist:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')

    return render(request, "verify-otp.html")

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

    try:
            verification_record = verification.objects.get(user=user)
            
            # If verified, update the user role to 'influencer'
            if verification_record.verifyed:
                user.user_role = 'influencer'
                user.save()  # Save the updated role
                
    except verification.DoesNotExist:
         pass  # If no verification record exists, nothing changes

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


    try:
            verification_record = verification.objects.get(user=user)
            
            # If verified, update the user role to 'influencer'
            if verification_record.verifyed:
                user.user_role = 'influencer'
                user.save()  # Save the updated role
            else:
                user.user_role = 'advertiser'
                user.save()    
                
    except verification.DoesNotExist:
         pass  # If no verification record exists, nothing changes    
    
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
            messages.success(request, "Your Report has been Submitted.")
            return redirect('scs_page')  # Redirect after successful submission

    except Exception as e:
        messages.error(request, "Something went wrong. Please try again.")
        print("Error:", e)  # Logs the actual error for debugging

    return render(request, 'report.html',{'user': user})


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
            messages.success(request, "Your Help Request has been Submitted.")
            return redirect('scs_page')  # Redirect after successful submission

    except Exception as e:
        messages.error(request, "Something went wrong. Please try again.")
        print("Error:", e)  # Logs the actual error for debugging

    return render(request, 'help.html',{'user': user})



def send_verification_email(mail_id):
    """Function to send a verification request confirmation email"""
    subject = "Your Verification Request Has Been Received"

    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Dear User,</p>
        <p>We have received your request for verification.</p>
        <p><b>Our team will review your request and notify you once the process is complete.</b></p>
        <p>For any updates, please check your email.</p>
        <br>
        img src="static/images/fluxify logo-01.svg" alt="verification" border="0">
        <p>Best regards,</p>
        <p><b>Flexify Team</b></p>
    </body>
    </html>
    """

    try:
        send_mail(
            subject,
            "",
            "fluxify.inc@gmail.com",  # Sender email
            [mail_id],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Failed to send email: {str(e)}")  # Debugging print



def verification_request(request):
    
    try:
        if not request.session.get('is_logged_in'):
            return redirect('login_page')

        user_email = request.session.get('mail_id')
        user = user_custome.objects.filter(mail_id=user_email).first()
        
        if not user:
            messages.error(request, "User not found.")
            return redirect('login_page')

        if request.method == "POST":
            instagram_id = request.POST.get("instagram_id", "").strip()
            x_id = request.POST.get("x_id", "").strip()
            youtube_name = request.POST.get("youtube_name", "").strip()

            if not instagram_id or not x_id or not youtube_name:
                messages.error(request, "All fields are required.")
                return redirect("verification_page")
            

            if verification.objects.filter(user=user).exists():
                messages.warning(request, "You have already submitted a verification request.")
                return redirect('scs_page')
            
            # Save the verification request
            verification.objects.create(
                user=user,
                instagram_id=instagram_id,
                x_id=x_id,
                youtube_name=youtube_name,
            )
            send_verification_email(user_email)
            messages.success(request, "Verification request submitted successfully.")
            return redirect("scs_page")

            
            
    except Exception as e:
        messages.error(request, "Something went wrong. Please try again.")
        print("Error:", e)  # Logs error for debugging

        
    return render(request, "verification_form.html")

def scs(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    
     # Retrieve the email from the session
    user_email=request.session.get('mail_id')
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first() 
    
    try:
        verification_record = verification.objects.get(user=user)
            
        # If verified, update the user role to 'influencer'
        if verification_record.verifyed:
                user.user_role = 'influencer'
                user.save()  # Save the updated role

        else:
                user.user_role = 'advertiser'
                user.save()    
                
    except verification.DoesNotExist:
         pass  # If no verification record exists, nothing changes
    
    return render(request, "sucsess.html" ,{'user': user})