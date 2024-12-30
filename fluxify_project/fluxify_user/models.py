from django.db import models

# Create your models here.
class user(models.model):
    mail_id=models.CharField(max_length=200)
    user_name=models.CharField(max_length=200)
    phone_no=models.CharField(max_length=10)
    pin_code=models.CharField(max_length=6)
    adress=models.TextField()
    profile_photo=models.ImageField(upload_to='/media')

    def __str__(self):
        return self.user_name
    