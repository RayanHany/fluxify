"""
URL configuration for fluxify_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [ 
    path('home', views.home,name='home_page'),
    path('settings', views.settings,name='settings_page'),
    path('profile', views.profile,name='profile_page'),
    path('login', views.login,name='login_page'),
    path('signup', views.signup,name='signup_page'),
    path('verify-otp/',views.verify_otp, name='verify_otp'),
    path('logout', views.user_logout,name='logout'),
    path('user/<id>', views.user_b,name='user_b_profile'),
    path('profile_saved', views.profile_page_saved, name='profile_page_saved'),
    path('save_post/<int:post_id>/', views.save_post, name='save_post'),
    path('report/', views.report_issue, name='report_issue'),
    path('help/', views.submit_help_request, name='submit_help_request'),
    path("verification/", views.verification_request, name="verification_page"),
    path("scs", views.scs, name="scs_page"),
    path("", views.index, name="index_page"),
    path("update-user/<int:user_id>/",views.update_user, name="update_user"),
    path("upload-profile-photo", views.upload_profile_photo, name="upload_profile_photo"),
    

    
    
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
