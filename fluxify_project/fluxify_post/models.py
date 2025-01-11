from django.db import models
from fluxify_user.models import user_custome
# Create your models here.
class post_mark(models.Model):
    post_image = models.ImageField(upload_to='posts/images/')
    posted_by = models.ForeignKey(user_custome, null=True, on_delete=models.CASCADE, related_name='posts')
    category = models.CharField(max_length=100)
    post_location = models.CharField(max_length=100)
    post_description = models.CharField(max_length=200)
    avg_price = models.FloatField()
    estimate_view = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.posted_by.user_name}"


class review(models.Model):
    post=models.ForeignKey(post_mark,null=False,on_delete=models.CASCADE,related_name='reviews')
    review_text=models.TextField()
    review_by=models.ForeignKey(user_custome,null=True,on_delete=models.SET_NULL,related_name='reviews')
    rating=models.FloatField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_by.user_name
