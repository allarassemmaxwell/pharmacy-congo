from django.urls import path
from .views import *


app_name = 'patient'

urlpatterns = [
    # ==================================================
    #                     DASHBOARD URLS
    # ==================================================
    path('', patient_view, name="home"),
    path('symptom/', symptom_view, name="symptom"),
    path('appointment/', appoitment_view, name="appointment"),
    path('appointment/add/', appointment_add_view, name="appointment_add"),
    path('appointment/edit/<str:id>/', appointment_update_view, name="appointment_update"),

    path('prescription/', prescription_view, name="prescription"),
 
]




