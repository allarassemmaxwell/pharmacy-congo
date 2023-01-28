from django.urls import path
from .views import *




app_name = 'landing'

urlpatterns = [
    path('', home_view, name="home"),
    path('about/', about_view, name="about"),
    path('contact/', contact_view, name="contact"),
    path('newsletter/', newsletter_view, name="subcriber"),
    path('blog/', blog_view, name="blog"),
    path('blog/<slug:slug>/', blog_detail_view, name="blog_detail"),
]




