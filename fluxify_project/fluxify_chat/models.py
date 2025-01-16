from django.db import models
from fluxify_user.models import user_custome

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(user_custome, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(user_custome, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.user_name} to {self.receiver.user_name} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']  # Messages are ordered by time.