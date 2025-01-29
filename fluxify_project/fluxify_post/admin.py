from django.contrib import admin
from atexit import register
from .models import post_mark
from django.utils.html import format_html
from django.apps import apps
from unfold.admin import ModelAdmin

Post_custome = apps.get_model('fluxify_post', 'post_mark')
Review = apps.get_model('fluxify_post', 'Review')
# Register your models here.
@admin.register(post_mark)
class PostMarkAdmin(ModelAdmin):
    # Add a custom method to display the image
    def display_post_image(self, obj):
        if obj.post_image:  # Check if the image exists
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />', 
                obj.post_image.url  # Use the image URL
            )
        return "No Image"
    
    # Update list_display to use the custom method
    list_display = (
        'display_post_image',  # Replace 'post_image' with this method
        'posted_by', 
        'category', 
        'post_location', 
        'avg_price', 
        'estimate_view', 
        'created_at'
    )
    display_post_image.short_description = 'Post Image'  # Column header name

admin.site.register(Review) 
