# import email
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import activate, gettext_lazy as _
from .forms import *
from .models import *
# from django.contrib import messages

from datetime import date, timedelta
import random
# from django.http import HttpResponse

from django.conf import settings
# from django.contrib.auth import get_user_model
# User = get_user_model()



# ==========================================================================
#                             LANDING VIEWS
# ==========================================================================
# Home page
def home_view(request):
    context  = {
        
    }
    template = "index.html"
    return render(request, template, context)







# Pharmacist Dashboard  page
def pharmacist_dashboard_view(request):
    context  = {
        
    }
    template = "pharmacist_dashboard.html"
    return render(request, template, context)