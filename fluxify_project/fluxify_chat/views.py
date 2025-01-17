from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Subquery, OuterRef
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Message
from fluxify_user.models import user_custome
from django.utils.timezone import now



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

    # Retrieve the email from the session
    user_email=request.session.get('mail_id')
        
    # Get the user object by matchig the email
    user=user_custome.objects.filter(mail_id=user_email).first() 

    return render(request, 'chat-page.html', {'users': users, 'user': user})




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

    print(f"Receiver username: {receiver}")

    # Render the chat template with receiver and messages
    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages,
    })



# AJAX endpoint to send a message
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            receiver_username = data.get("receiver")
            content = data.get("content")

            sender = get_current_user(request)
            if not sender:
                return JsonResponse({"error": "User not logged in"}, status=401)

            receiver = get_object_or_404(user_custome, user_name=receiver_username)

            # Create and save the message
            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                timestamp=now(),
            )

            return JsonResponse({"status": "success", "message_id": message.id}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# AJAX endpoint to fetch new messages
def fetch_messages(request, user):
    if not request.session.get('is_logged_in'):
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    current_user = get_current_user(request)
    if not current_user:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    receiver = get_object_or_404(user_custome, id=user)

    messages = Message.objects.filter(
        Q(sender=current_user, receiver=receiver) |
        Q(sender=receiver, receiver=current_user)
    ).order_by('timestamp')

    return JsonResponse({'messages': [
        {
            'sender': message.sender.user_name,
            'receiver': message.receiver.user_name,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for message in messages
    ]}, status=200)