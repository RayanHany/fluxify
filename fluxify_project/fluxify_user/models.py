from django.db import models
from django.core.validators import MinLengthValidator
#from django.contrib.auth.models import AbstractUser
from django import forms
from django.utils.timezone import now  # Import now()


# Create your models here.


class user_custome(models.Model):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('publisher', 'Publisher'),
        ('influencer', 'Influencer'),
        ('advertiser', 'Advertiser'),
    ]
    
    mail_id=models.CharField(max_length=200,unique=True)
    password=models.CharField( max_length=100,validators=[MinLengthValidator(8)])
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default='advertiser')
    user_name=models.CharField(max_length=200,unique=True)
    phone_no=models.CharField(max_length=10,unique=True)
    pin_code=models.CharField(max_length=6)
    address=models.TextField()
    profile_photo=models.ImageField(upload_to="images/",null=True, blank=True, default='/images/default-avatar.png')
        # Property method to return the default image if no profile picture is uploaded
    def get_profile_Photo(self):
        if self.profile_Photo:
            return self.profile_Photo.url
        # Default image URL if no profile picture is uploaded
        return '/static/images/default-avatar.png'

    # Optionally, use this in the admin panel or other places
    profile_Photo_url = property(get_profile_Photo)

    def __str__(self):
        return self.user_name
    


class OTPVerification(models.Model):
    user = models.ForeignKey(user_custome, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (now() - self.created_at).seconds < 300  # OTP valid for 5 minutes

    def __str__(self):
        return f"OTP for {self.user.mail_id}"
    
class report(models.Model):
    user=models.ForeignKey(user_custome,null=True,on_delete=models.SET_NULL,related_name='reports_user')
    report_image=models.ImageField(upload_to="images/")
    report_text=models.TextField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user_name
    

class help(models.Model):
    user=models.ForeignKey(user_custome,null=True,on_delete=models.CASCADE,related_name='help_user')
    help_image=models.ImageField(upload_to='media/')
    help_text=models.TextField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user_name
    
class verification(models.Model):
    user=models.ForeignKey(user_custome,null=True,on_delete=models.CASCADE,related_name='verification_user')
    verifyed=models.BooleanField(default=False)
    instagram_id=models.CharField(max_length=200,null=False)
    x_id=models.CharField(max_length=200,null=False)
    youtube_name=models.CharField(max_length=200,null=False)

    def __str__(self):
        return self.user.user_name
    

class SavedPost(models.Model):
    user=models.ForeignKey(user_custome,null=True,on_delete=models.CASCADE,related_name='saved_user')
    post = models.ForeignKey('fluxify_post.Post_mark', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.post}"