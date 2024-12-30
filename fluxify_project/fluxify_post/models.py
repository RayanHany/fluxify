from django.db import models
from fluxify_user.models import user_name
# Create your models here.
class post(models.Model):
    leve=1
    delete=0
    delete_choices=((live,'live')),(delete,'delete')
    posted_by=models.ForeignKey(user_name)
    catagory=models.CharField(max_length=100)
    post_location=models.CharField(max_length=100)
    post_description=models.CharField(max_length=200)
    avg_price=models.FloatField()
    estimate_view=models.IntegerField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name


