from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.utils.html import format_html
from django.apps import apps
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from unfold.admin import ModelAdmin
from .models import post_mark

Post_custome = apps.get_model('fluxify_post', 'post_mark')
Review = apps.get_model('fluxify_post', 'Review')

class PostMarkAdmin(ModelAdmin):
    def display_post_image(self, obj):
        if obj.post_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />', 
                obj.post_image.url
            )
        return "No Image"

    display_post_image.short_description = 'Post Image'

    list_display = ('display_post_image', 'posted_by', 'category', 'post_location', 'avg_price', 'estimate_view', 'created_at')
    list_filter = ('category', 'post_location', 'avg_price')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-pdf/', self.export_pdf, name='post_mark_export_pdf'),
        ]
        return custom_urls + urls

    def export_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="post_mark_data.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        data = [['Post Image', 'Posted By', 'Category', 'Location', 'Avg Price', 'Estimated View', 'Created At']]
        queryset = self.get_queryset(request)
        for post in queryset:
            data.append([
                post.post_image.url if post.post_image else "No Image",
                post.posted_by.user_name,  
                post.category,
                post.post_location,
                f"₹{post.avg_price}",
                post.estimate_view,
                post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    def export_pdf_button(self, request, queryset):
        return self.export_pdf(request)

    export_pdf_button.short_description = "Export PDF"
    
    actions = ['export_pdf_button']  # Fix: Now it works properly

admin.site.register(post_mark, PostMarkAdmin)
