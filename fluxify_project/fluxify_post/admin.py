from django.contrib import admin
from atexit import register
from .models import post_mark


from django.apps import apps
Post_custome = apps.get_model('fluxify_post', 'post_mark')
Review = apps.get_model('fluxify_post', 'Review')
# Register your models here.
@admin.register(post_mark)
class PostMarkAdmin(admin.ModelAdmin):
    list_display = ('post_image', 'posted_by', 'category', 'post_location', 'avg_price', 'estimate_view', 'created_at')
admin.site.register(Review) 
