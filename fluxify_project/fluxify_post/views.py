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
    
    # Retrieve the email from the session
    user_email = request.session.get('mail_id')
        
    # Get the user object using the email
    user = user_custome.objects.get(mail_id=user_email)

    
    return render(request, 'listing-page.html',{'user': user})



def post_search(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    return render(request, 'post_search.html')



def post_sort(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    
    # Retrieve the email from the session
    user_email=request.session.get('mail_id')
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first() 
    return render(request, 'post_sort.html' ,{'user':user })



def sorted_posts(request):

    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    

    # Retrieve the email from the session
    user_email=request.session.get('mail_id')
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first() 
    
    # Retrieve filtering and sorting criteria from GET parameters
    category = request.GET.get('category', '')  # Default to empty string
    location = request.GET.get('location', '')  # Default to empty string
    price_order = request.GET.get('price', '')  # Can be 'asc' or 'desc'

    # Start with all posts
    posts = post_mark.objects.all()

    # Apply filters if provided
    if category:
        posts = posts.filter(category__icontains=category)  # Filter by category (case-insensitive)
    if location:
        posts = posts.filter(post_location__icontains=location)  # Filter by location (case-insensitive)

    # Apply sorting if provided
    if price_order == 'asc':
        posts = posts.order_by('avg_price')  # Sort by price (ascending)
    elif price_order == 'desc':
        posts = posts.order_by('-avg_price')  # Sort by price (descending)

    # Render the sorted and filtered posts
    return render(request, 'sorted-posts.html', {'user': user ,'posts': posts})



def keyword_search(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')

    query = request.GET.get('q', '')  # Retrieve the search keyword from the query string
    posts = []
    users = []
    error_message = "An error occurred while processing your search. Please try again later."

    try:
        if query:
            # Filter posts based on the search keyword
            posts = post_mark.objects.filter(
                Q(category__icontains=query) |
                Q(post_location__icontains=query) |
                Q(post_description__icontains=query)
            )
            
            # Filter users based on the search keyword
            users = user_custome.objects.filter(
                Q(user_name__icontains=query) |
                Q(mail_id__icontains=query) |
                Q(address__icontains=query)
            )

            for user in users:
                if not user.profile_photo:  # If there's no profile photo
                    user.profile_photo = 'images/default-avatar.png'  # Set default image path

            # Retrieve the email from the session
            user_email = request.session.get('mail_id')
                
            # Get the user object by matching the email
            user = user_custome.objects.filter(mail_id=user_email).first()

    except Exception as e:
        # Log the error (optional) and set the error message
        print(f"Error during search: {e}")
        error_message = "An unexpected error occurred while processing your search."

    # Render the search results page
    return render(request, 'search_results.html', {
        'query': query,
        'posts': posts,
        'users': users,
        'user': user,
        'error_message': error_message,
    })



def post_details(request,id):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')
    post=post_mark.objects.get(id=id)

    # Retrieve the email from the session
    user_email=request.session.get('mail_id')
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first() 

    context = {'user': user,'post': post}

    return render(request, 'post-detailed-page.html',context)