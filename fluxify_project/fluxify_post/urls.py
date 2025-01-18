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
from fluxify_user import urls
from . import views
urlpatterns = [
    path('list', views.list,name='list_page'),
    path('posts_search', views.post_search, name='post_search'),
    path('post_sort', views.post_sort, name='post_sort'),  # Sorting page
    path('sorted-posts', views.sorted_posts, name='sorted_posts'),  # Target page
    path('search/', views.keyword_search, name='keyword_search'),
    path('post_details/<int:id>/', views.post_details, name='post_details'),
    


    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
