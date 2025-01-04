from django.db import models
from fluxify_user.models import user
# Create your models here.
class post(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = (
        (LIVE, 'Live'),
        (DELETE, 'Delete'),
    )
    
    post_image = models.ImageField(upload_to='media/')
    posted_by = models.ForeignKey(user, null=True, on_delete=models.SET_NULL, related_name='posts')
    category = models.CharField(max_length=100)  # Fixed typo: 'catagory' -> 'category'
    post_location = models.CharField(max_length=100)
    post_description = models.CharField(max_length=200)
    avg_price = models.FloatField()
    estimate_view = models.IntegerField()
    status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)  # Added status field with choices
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.posted_by.user_name}"


class review(models.Model):
    post=models.ForeignKey(post,null=False,on_delete=models.CASCADE,related_name='reviews')
    review_text=models.TextField()
    review_by=models.ForeignKey(user,null=True,on_delete=models.SET_NULL,related_name='reviews')
    rating=models.FloatField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_by.user_name
