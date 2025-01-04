from django.contrib import admin
from atexit import register
from django.apps import apps
Post = apps.get_model('fluxify_post', 'Post')
Review = apps.get_model('fluxify_post', 'Review')
# Register your models here.
admin.site,register(Post)
admin.site.register(Review) 
