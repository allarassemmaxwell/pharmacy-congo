from django.urls import path
from .views import *


app_name = 'patient'

urlpatterns = [
    # ==================================================
    #                     DASHBOARD URLS
    # ==================================================
    path('', dashboard_view, name="home"),
 
]




