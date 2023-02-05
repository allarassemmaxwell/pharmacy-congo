from django.urls import path
from .views import *
# from .api import *
urlpatterns = [
    # ==================================================
    #                     DASHBOARD URLS
    # ==================================================
    path('', dashboard_view, name="dashboard"),
    path('profile/', profile_view, name="profile"),
    path('blog/', blog_view, name="blog"),
    path('blog/add/', blog_add_view, name="blog_add"),

    path('blog-category/', blog_category_view, name="blog_category"),
    path('blog-category/add/', blog_category_add_view, name="blog_category_add"),

    path('contacts/', contact_view, name="contact"),

    path('newsletters/', newsletter_view, name="newsletter"),
    path('newsletters/add/', newsletter_add_view, name="newsletter_add"),

    path('partner/', partner_view, name="partner"),
    path('partner/add/', partner_add_view, name="partner_add"),

    path('testimony/', testimony_view, name="testimony"),
    path('testimony/add/', testimony_add_view, name="testimony_add"),

    path('user/', user_view, name="user"),
    # path('testimony/add/', testimony_add_view, name="testimony_add"),

    path('product/', product_view, name="product"),
]




