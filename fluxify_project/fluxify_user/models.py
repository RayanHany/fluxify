from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class user_custome(models.Model):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('publisher', 'Publisher'),
        ('influencer', 'Influencer'),
        ('advertiser', 'Advertiser'),
    ]
    
    mail_id=models.CharField(max_length=200)
    password=models.CharField( max_length=50,validators=[MinLengthValidator(8)])
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default='advertiser')
    user_name=models.CharField(max_length=200)
    phone_no=models.CharField(max_length=10)
    pin_code=models.CharField(max_length=6)
    adress=models.TextField()
    profile_photo=models.ImageField(upload_to='media/')

    def __str__(self):
        return self.user_name
    
class report(models.Model):
    user=models.ForeignKey(user_custome,null=True,on_delete=models.SET_NULL,related_name='reports')
    report_image=models.ImageField(upload_to='media/')
    report_text=models.TextField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user_name
    

class help(models.Model):
    user=models.ForeignKey(user_custome,null=True,on_delete=models.CASCADE,related_name='help')
    help_image=models.ImageField(upload_to='media/')
    help_text=models.TextField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user_name
    
class verification(models.Model):
    user=models.ForeignKey(user_custome,null=True,on_delete=models.CASCADE,related_name='verificatio')
    verifyed=models.BooleanField(default=False)
    instagram_id=models.CharField(max_length=200,null=False)
    x_id=models.CharField(max_length=200,null=False)
    youtube_name=models.CharField(max_length=200,null=False)

    def __str__(self):
        return self.user.user_name
    
    from django.contrib.auth.models import AbstractUser
from django.db import models

