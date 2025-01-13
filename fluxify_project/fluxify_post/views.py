from django.shortcuts import render,redirect
from .models import post_mark
from fluxify_user.models import user_custome
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def list(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    if request.method == 'POST':
        # Retrieve the email from the session
        user_email = request.session.get('mail_id')
        
        # Get the user object using the email
        user = user_custome.objects.get(mail_id=user_email)


        # Get other post details from the form
        post_image = request.FILES.get('post_image')
        category = request.POST.get('category')
        post_location = request.POST.get('post_location')
        post_description = request.POST.get('post_description')
        avg_price = request.POST.get('avg_price')
        estimate_view = request.POST.get('estimate_view')

        # Create and save the post
        post = post_mark(
            post_image=post_image,
            posted_by=user,  # Link the user using the email
            category=category,
            post_location=post_location,
            post_description=post_description,
            avg_price=avg_price,
            estimate_view=estimate_view,
        )
        post.save()
        # Update user's role to 'publisher' if it's not already
        if user.user_role != 'publisher':
            user.user_role = 'publisher'
            user.save()  # Save changes to the database
        return redirect('home_page')  # Redirect after saving the post
    return render(request, 'listing-page.html')



def post_search(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    return render(request, 'post_search.html')



def post_sort(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    return render(request, 'post_sort.html')
