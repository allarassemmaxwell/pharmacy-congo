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

from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from landing_app.models import *

# import requests
# import json
# import hashlib


from decimal import Decimal
import datetime
# from dateutil.relativedelta import relativedelta

from functools import wraps

from landing_app.models import *

from .forms import *





class PasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')



# ==================================================
#                     DASHBOARD VIEWS
# ==================================================
# DASHBOARD VIEW 
@login_required
def dashboard_view(request):
    context = {
    }
    template = "dashboard/index.html"
    return render(request,template,context)

    




@login_required
def profile_view(request):
    context  = {}
    template = "dashboard/profile/profile.html"
    return render(request, template, context)





# BLOG VIEW 
@login_required
def blog_view(request):
    blogs    = Blog.objects.all()
    context = {'blogs': blogs}
    template = "dashboard/blog/blog.html"
    return render(request, template, context)






# BLOG VIEW 
@login_required
def blog_add_view(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            # organization = BlogCategory.objects.get(user=request.user)
            # obj = form.save(commit=False)
            # obj.organization = organization
            form.save()
            messages.success(request, _("Blog créé avec succès."))
            return redirect('blog')
    else:
        form = BlogForm()

    context = {'form': form}
    template = "dashboard/blog/blog-add.html"
    return render(request, template, context)







# BLOG VIEW 
@login_required
def blog_category_view(request):
    categories = BlogCategory.objects.all()

    # PAGINATION 
    # paginator = Paginator(blogs, 9)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {'categories': categories}
    template = "dashboard/blog/category.html"
    return render(request, template, context)




# BLOG VIEW 
@login_required
def blog_category_add_view(request):
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Blog Catégorie créé avec succès."))
            return redirect('blog_category')
    else:
        form = BlogCategoryForm()

    context = {'form': form}
    template = "dashboard/blog/category-add.html"
    return render(request, template, context)








# BLOG VIEW 
@login_required
def contact_view(request):
    contacts    = Contact.objects.all()
    context = {'contacts': contacts}
    template = "dashboard/contact.html"
    return render(request, template, context)





# BLOG VIEW 
@login_required
def newsletter_view(request):
    newsletters    = Subscriber.objects.all()
    context = {'newsletters': newsletters}
    template = "dashboard/newsletter/newsletter.html"
    return render(request, template, context)





# BLOG VIEW 
@login_required
def newsletter_add_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Témoignage créé avec succès."))
            return redirect('newsletter')
    else:
        form = NewsletterForm()

    context = {'form': form}
    template = "dashboard/newsletter/newsletter-add.html"
    return render(request, template, context)







# BLOG VIEW 
@login_required
def partner_view(request):
    partners    = Partner.objects.all()
    context = {'partners': partners}
    template = "dashboard/partner/partner.html"
    return render(request, template, context)





# BLOG VIEW 
@login_required
def partner_add_view(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Partenaire créé avec succès."))
            return redirect('partner')
    else:
        form = PartnerForm()

    context = {'form': form}
    template = "dashboard/partner/partner-add.html"
    return render(request, template, context)






# BLOG VIEW 
@login_required
def testimony_view(request):
    testimonies    = Testimony.objects.all()
    context = {'testimonies': testimonies}
    template = "dashboard/testimony/testimony.html"
    return render(request, template, context)







# BLOG VIEW 
@login_required
def testimony_add_view(request):
    if request.method == 'POST':
        form = TestimonyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Témoignage créé avec succès."))
            return redirect('testimony')
    else:
        form = TestimonyForm()

    context = {'form': form}
    template = "dashboard/testimony/testimony-add.html"
    return render(request, template, context)







# BLOG VIEW 
@login_required
def user_view(request):
    users    = User.objects.all()
    context = {'users': users}
    template = "dashboard/user/user.html"
    return render(request, template, context)





# BLOG VIEW 
@login_required
def product_view(request):
    blogs    = Blog.objects.all()
    context = {'blogs': blogs}
    template = "dashboard/product/product.html"
    return render(request, template, context)




