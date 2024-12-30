from django.db import models
from fluxify_user.models import user
# Create your models here.
class post(models.Model):
    live=1
    delete=0
    delete_choices=((live,'live')),(delete,'delete')
    post_image=models.ImageField(upload_to='/media/post_images')
    posted_by=models.ForeignKey(user,null=False,on_delete=models.SET_NULL,related_name='posts')
    catagory=models.CharField(max_length=100)
    post_location=models.CharField(max_length=100)
    post_description=models.CharField(max_length=200)
    avg_price=models.FloatField()
    estimate_view=models.IntegerField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.posted_by.user_name


class review(models.Model):
    post=models.ForeignKey(post,null=False,on_delete=models.CASCADE,related_name='reviews')
    review_text=models.TextField()
    review_by=models.ForeignKey(user,null=False,on_delete=models.SET_NULL,related_name='reviews')
    rating=models.FloatField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_by.user_name
