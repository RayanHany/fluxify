from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import user_custome, report, help, verification, SavedPost
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_pdf(users):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="user_data.pdf"'
    
    pdf = canvas.Canvas(response)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 800, "User Custom Data Report")
    pdf.setFont("Helvetica", 10)
    
    y = 780
    for user in users:
        pdf.drawString(50, y, f"ID: {user.id}, Name: {user.user_name}, Email: {user.mail_id}, Role: {user.user_role}, Phone: {user.phone_no}, Pincode: {user.pin_code}")
        y -= 20
        if y < 50:  # New page if content exceeds
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = 800
    
    pdf.save()
    return response

# Custom admin action
def download_users_as_pdf(modeladmin, request, queryset):
    return generate_pdf(queryset)

download_users_as_pdf.short_description = "Download selected users as PDF"

# UserCustome Admin
@admin.register(user_custome)
class UserCustomeAdmin(ModelAdmin):
    list_display = ('id', 'user_name', 'mail_id', 'user_role', 'phone_no', 'pin_code')
    search_fields = ('user_name', 'mail_id', 'phone_no')
    list_filter = ('user_role',)
    readonly_fields = ('profile_Photo_url',)
    actions = [download_users_as_pdf]  # Adding the action to the admin panel

    def profile_Photo_url(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.profile_photo.url if obj.profile_photo else '/static/images/default-avatar.png')
    
    profile_Photo_url.short_description = 'Profile Photo'

# Report Admin
@admin.register(report)
class ReportAdmin(ModelAdmin):
    list_display = ('id', 'user', 'report_image_preview', 'report_text_short', 'created_at')
    search_fields = ('user__user_name', 'report_text')
    list_filter = ('created_at',)

    def report_image_preview(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.report_image.url) if obj.report_image else ''
    report_image_preview.short_description = 'Image'

    def report_text_short(self, obj):
        return f"{obj.report_text[:50]}..." if len(obj.report_text) > 50 else obj.report_text
    report_text_short.short_description = 'Report Text'

# Help Admin
@admin.register(help)
class HelpAdmin(ModelAdmin):
    list_display = ('id', 'user', 'help_image_preview', 'help_text_short', 'created_at')
    search_fields = ('user__user_name', 'help_text')
    list_filter = ('created_at',)

    def help_image_preview(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.help_image.url) if obj.help_image else ''
    help_image_preview.short_description = 'Image'

    def help_text_short(self, obj):
        return f"{obj.help_text[:50]}..." if len(obj.help_text) > 50 else obj.help_text
    help_text_short.short_description = 'Help Text'

# Verification Admin
@admin.register(verification)
class VerificationAdmin(ModelAdmin):
    list_display = ('id', 'user', 'verifyed', 'instagram_id', 'x_id', 'youtube_name')
    list_filter = ('verifyed',)
    search_fields = ('user__user_name', 'instagram_id', 'x_id')
    raw_id_fields = ('user',)

# SavedPost Admin
@admin.register(SavedPost)
class SavedPostAdmin(ModelAdmin):
    list_display = ('id', 'user', 'post', 'saved_at')
    search_fields = ('user__user_name', 'post__id')
    list_filter = ('saved_at',)
    raw_id_fields = ('user', 'post')