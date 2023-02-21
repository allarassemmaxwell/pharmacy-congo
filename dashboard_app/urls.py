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
    path('blog/delete/<slug:slug>/', blog_delete_view, name="blog_delete"),
    path('blog/update/<slug:slug>/', blog_update_view, name="blog_update"),

    path('blog-category/', blog_category_view, name="blog_category"),
    path('blog-category/add/', blog_category_add_view, name="blog_category_add"),
    path('blog-category/delete/<slug:slug>/', blog_category_delete_view, name="blog_category_delete"),
    path('blog-category/update/<slug:slug>/', blog_category_update_view, name="blog_category_update"),

    

    path('contacts/', contact_view, name="contact"),
    path('contacts/add/', contact_add_view, name="contact_add"),
    path('contacts/delete/<int:id>/', contact_delete_view, name="contact_delete"),
    path('contacts/update/<int:id>/', contact_update_view, name="contact_update"),

    path('newsletters/', newsletter_view, name="newsletter"),
    path('newsletters/add/', newsletter_add_view, name="newsletter_add"),
    path('newsletters/delete/<int:id>/', newsletter_delete_view, name="newsletter_delete"),
    path('newsletters/update/<int:id>/', newsletter_update_view, name="newsletter_update"),

    path('partner/', partner_view, name="partner"),
    path('partner/add/', partner_add_view, name="partner_add"),
    path('partner/delete/<slug:slug>/', partner_delete_view, name="partner_delete"),
    path('partner/update/<slug:slug>/', partner_update_view, name="partner_update"),

    path('testimony/', testimony_view, name="testimony"),
    path('testimony/add/', testimony_add_view, name="testimony_add"),
    path('testimony/delete/<int:id>/', testimony_delete_view, name="testimony_delete"),
    path('testimony/update/<int:id>/', testimony_update_view, name="testimony_update"),

    path('user/', user_view, name="user"),
    path('user/add/', user_add_view, name="user_add"),
    path('user/delete/<slug:slug>/', user_delete_view, name="user_delete"),
    path('user/update/<slug:slug>/', user_update_view, name="user_update"),
    # path('testimony/add/', testimony_add_view, name="testimony_add"),


    
    path('service/category/', service_category_view, name="service_category"),
    path('service/category/delete/<slug:slug>/', service_category_delete_view, name="service_category_delete"),
    path('service/category/update/<slug:slug>/', service_category_update_view, name="service_category_update"),

    path('service/', service_view, name="service"),
    path('service/add/', service_add_view, name="service_add"),
    path('service/delete/<slug:slug>/', service_delete_view, name="service_delete"),
    path('service/update/<slug:slug>/', service_update_view, name="service_update"),
    

    path('product/', product_view, name="product"),
    path('product/add/', product_add_view, name="product_add"),
    path('product/delete/<slug:slug>/', product_delete_view, name="product_delete"),
    path('product/update/<slug:slug>/', product_update_view, name="product_update"),

    path('product/image/', product_image_view, name="product_image"),
    path('product/image/delete/<slug:slug>/', product_image_delete_view, name="product_image_delete"),
    path('product/image/update/<slug:slug>/', product_image_update_view, name="product_image_update"),



    path('product/category/', product_category_view, name="product_category"),
    path('product/category/delete/<slug:slug>/', product_category_delete_view, name="product_category_delete"),
    path('product/category/update/<slug:slug>/', product_category_update_view, name="product_category_update"),


    path('supplier/', supplier_view, name="supplier"),
    path('supplier/add/', supplier_add_view, name="supplier_add"),
    path('supplier/delete/<slug:slug>/', supplier_delete_view, name="supplier_delete"),
    path('supplier/update/<slug:slug>/', supplier_update_view, name="supplier_update"),
    
    
    path('stock/', stock_view, name="stock"),
    path('stock/add/', stock_add_view, name="stock_add"),
    path('stock/delete/<str:id>/', stock_delete_view, name="stock_delete"),
    path('stock/update/<str:id>/', stock_update_view, name="stock_update"),
    
    
    path('appointment/symptoms/', appointment_symptom_view, name="appointment_symptom"),
    path('appointment/symptoms/delete/<slug:slug>/', appointment_symptom_delete_view, name="appointment_symptom_delete"),
    path('appointment/symptoms/update/<slug:slug>/', appointment_symptom_update_view, name="appointment_symptom_update"),

    path('appointment/', appointment_view, name="appointment"),
    path('appointment/add', appointment_add_view, name="appointment_add"),
    path('appointment/delete/<str:id>/', appointment_delete_view, name="appointment_delete"),
    path('appointment/update/<str:id>/', appointment_update_view, name="appointment_update"),


    path('appointment/prescription/', appointment_prescription_view, name="appointment_prescription"),
    path('appointment/prescription/add/', appointment_prescription_add_view, name="appointment_prescription_add"),
    path('appointment/prescription/delete/<int:id>/', appointment_prescription_delete_view, name="appointment_prescription_delete"),
    path('appointment/prescription/update/<int:id>/', appointment_prescription_update_view, name="appointment_prescription_update"),

    path('patient/', patient_view, name="patient"),
]




