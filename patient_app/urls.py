from django.urls import path
from .views import *
# from .api import *
urlpatterns = [
    # ==================================================
    #                     DASHBOARD URLS
    # ==================================================
    path('', dashboard_view, name="patient"),
 
]




