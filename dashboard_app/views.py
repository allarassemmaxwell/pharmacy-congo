from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import activate, gettext_lazy as _

# from .forms import *
from .models import *
# from .serializers import *
# from .utils import *

from django.contrib import messages

from datetime import date, timedelta
import random
from django.http import HttpResponse


from django.http import Http404
from django.core.paginator import Paginator
from django.conf import settings

from django.db.models import Q

from decimal import Decimal
# from paypal.standard.forms import PayPalPaymentsForm

from django.views.decorators.csrf import csrf_exempt

# from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy


# import requests
# import json
# import hashlib


from decimal import Decimal
import datetime
# from dateutil.relativedelta import relativedelta

from functools import wraps









# ==================================================
#                     DASHBOARD VIEWS
# ==================================================
# DASHBOARD VIEW 
@login_required
# @user_access_only()
def dashboard_view(request, *args, **kwargs):
    context = {
    }
    template = "dashboard/index.html"
    return render(request,template,context)

    

