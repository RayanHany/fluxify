from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Subquery, OuterRef
from django.views.decorators.csrf import csrf_exempt
import json
from .models import user_custome, Message



# Function to fetch the current user from the session
def get_current_user(request):
    mail_id = request.session.get('mail_id')
    if not mail_id:
        return None
    return get_object_or_404(user_custome, mail_id=mail_id)




# Chat index page
def chat(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')

    current_user = get_current_user(request)
    if not current_user:
        return redirect('login_page')

    # Fetch users sorted by the latest message timestamp
    users = (
        user_custome.objects.exclude(id=current_user.id)
        .annotate(
            latest_message=Subquery(
                Message.objects.filter(
                    Q(sender=current_user) | Q(receiver=current_user),
                    Q(sender=OuterRef('id')) | Q(receiver=OuterRef('id'))
                )
                .order_by("-timestamp")
                .values("content")[:1]
            )
        )
        .order_by("-latest_message")
    )

    return render(request, 'chat-page.html', {'users': users})




# View to render the chat page for a specific user
def chat_view(request, user):
    if not request.session.get('is_logged_in'):
        return redirect('login_page')

    current_user = get_current_user(request)
    if not current_user:
        return redirect('login_page')

    # Fetch the receiver user object based on the user.id from the URL
    receiver = get_object_or_404(user_custome, id=user)  # Use id instead of user_name

    # Fetch messages between the current user and the receiver
    messages = Message.objects.filter(
        Q(sender=current_user, receiver=receiver) |
        Q(sender=receiver, receiver=current_user)
    ).order_by('timestamp')

    # Render the chat template with receiver and messages
    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages,
    })