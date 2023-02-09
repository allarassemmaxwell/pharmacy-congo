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


    path('service/', service_view, name="service"),
    path('service/category/', service_category_view, name="service_category"),
    path('service/add/', service_add_view, name="service_add"),
    path('service/delete/<slug:slug>/', service_delete_view, name="service_delete"),
    path('service/category/delete/<slug:slug>/', service_category_delete_view, name="service_category_delete"),

    path('product/', product_view, name="product"),
    path('product/add/', product_add_view, name="product_add"),
    path('product/image/', product_image_view, name="product_image"),
    path('product/image/delete/<int:id>/', product_image_delete_view, name="product_image_delete"),

    path('product/delete/<slug:slug>/', product_delete_view, name="product_delete"),
    path('product/category/', product_category_view, name="product_category"),
    path('product/category/delete/<slug:slug>/', product_category_delete_view, name="product_category_delete"),


    path('supplier/', supplier_view, name="supplier"),
    path('supplier/add/', supplier_add_view, name="supplier_add"),
    path('supplier/delete/<slug:slug>/', supplier_delete_view, name="supplier_delete"),
    
    
    path('stock/', stock_view, name="stock"),
    path('stock/add/', stock_add_view, name="stock_add"),


]




