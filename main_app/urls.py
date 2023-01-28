from django.urls import path
from .views import *

urlpatterns = [
# Create your views here.
# ==========================================================================
#                             DASHBOARD URLS
# ==========================================================================

# Home page
path('home/', home_view, name="home"),
path('pharmacist-dashboard/', pharmacist_dashboard_view, name="pharmacist_dashboard"),

]