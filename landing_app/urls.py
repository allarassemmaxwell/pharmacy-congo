from django.urls import path
from .views import *




app_name = 'landing'

urlpatterns = [
    path('', home_view, name="home"),
    path('about/', about_view, name="about"),
    path('contact/', contact_view, name="contact"),
    path('pharmacy/', pharmacy_view, name="pharmacy"),
    path('product/', product_view, name="product"),
    path('product-list/', product_list_view, name="product_list"),
    path('product-detail/<slug:slug>/', product_detail_view, name="product_detail"),
    path('pharmacy-register/', pharmacy_register_view, name="pharmacy_register"),
    path('pharmacy-login/', pharmacy_login_view, name="pharmacy_login"),
    path('forgot-password/', forgot_password_view, name="forgot_password"),
    path('pharmacy-search/', pharmacy_search_view, name="pharmacy_search"),
    path('pharmacy-detail/', pharmacy_detail_view, name="pharmacy_detail"),
    path('newsletter/', newsletter_view, name="subcriber"),
    path('blog/', blog_view, name="blog"),
    path('blog/<slug:slug>/', blog_detail_view, name="blog_detail"),
    
    # Dashboard Pharmacist
    path('pharmacist-dashboard/', pharmacist_dashboard_view, name="pharmacist_dashboard"),
    path('pharmacist-add-profile/', phcist_add_profile_view, name="phcist_add_profile"),
    path('pharmacist-appointment/', phcist_appointment_view, name="phcist_appointment"),
    path('pharmacist-patient/', phcist_patient_view, name="phcist_patient"),
    path('pharmacist-patient-profile/', phcist_patient_profile_view, name="phcist_patient_profile"),
    path('add-prescription/', add_prescription_view, name="add_prescription"),
    path('add-billing/', add_billing_view, name="add_billing"),
    path('pharmacist-invoice/', phcist_invoice_view, name="phcist_invoice"),
    path('pharmacist-show-invoice/', phcist_show_invoice_view, name="phcist_show_invoice"),
    path('pharmacist-register/', phcist_register_view, name="phcist_register"),
    path('pharmacist-login/', phcist_login_view, name="phcist_login"),
    path('pharmacist-add-blog/', phcist_add_blog_view, name="phcist_add_blog"),
    
    # Dashboard Client
    path('patient-dashboard/', patient_dashboard_view, name="patient_dashboard"),
    path('search-pharmacist/', search_pharmacist_view, name="search_pharmacist"),
    path('pharmacist-profile/', phcist_profile_view, name="pharmacist_profile"),
    path('patient-checkout/', checkout_view, name="patient_checkout"),
    path('patient-booking/', booking_view, name="patient_booking"),
    path('favorite-pharmacist/', favorite_pharmacist_view, name="favorite_pharmacist"),
    path('patient-add-profile/', patient_add_profile_view, name="patient_add_profile"),
    path('patient-change-password/', patient_change_password_view, name="patient_change_password"),
    
    
    # Admin Pharmacy
    path('admin-pharmacy/', pharmacy_admin_view, name="pharmacy_admin"),
]




