from django.contrib import admin
from atexit import register
from django.apps import apps
user_custome = apps.get_model('fluxify_user', 'user_custome')
report = apps.get_model('fluxify_user', 'report')
help = apps.get_model('fluxify_user', 'help')
verification = apps.get_model('fluxify_user', 'verification')
# Register your models here.


admin.site.register(report)
admin.site.register(help) 
admin.site.register(verification) 
admin.site.register(user_custome)
