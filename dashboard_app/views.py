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






# SERVICE VIEW 
@login_required
def service_view(request):
    services    = Service.objects.all()
    context = {
        'services': services,
    }
    template = "dashboard/service/service.html"
    return render(request, template, context)




# PRODUCT ADD VIEW 
@login_required
def service_add_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Service créé avec succès."))
            return redirect('service')
    else:
        form = ServiceForm()

    context = {'form': form}
    template = "dashboard/service/service-add.html"
    return render(request, template, context)





# PRODUCT DELETE VIEW

# @login_required
# def service_delete_view(request, slug=None):
#     caregory = get_object_or_404(Service, slug=slug, active=True)
#     caregory.delete()
#     messages.success(request, _("Category deleted successfully."))
#     return redirect('service')





# BLOG VIEW 
@login_required
def service_category_view(request):
    categories    = ServiceCategory.objects.all()
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Category créé avec succès."))
            return redirect('service_category')
    else:
        form = ServiceCategoryForm()
    context = {
        'categories': categories,
        'form': form
    }
    template = "dashboard/service/category.html"
    return render(request, template, context)





@login_required
def service_category_delete_view(request, slug=None):
    category = get_object_or_404(ServiceCategory, slug=slug, active=True)
    category.delete()
    messages.success(request, _("Category deleted successfully."))
    return redirect('service_category')





# SERVICE DELETE VIEW

@login_required
def service_delete_view(request, slug=None):
    service = get_object_or_404(Service, slug=slug, active=True)
    service.delete()
    messages.success(request, _("Service deleted successfully."))
    return redirect('service')




# PRODUCT IMAGE VIEW 
@login_required
def product_image_view(request):
    images    = ProductImage.objects.all()
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Image ajoutée avec succès."))
            return redirect('product_image')
    else:
        form = ProductImageForm()
    context = {
        'images': images,
        'form': form
    }
    template = "dashboard/product/image.html"
    return render(request, template, context)




# PRODUCT IMAGE DELETE

@login_required
def product_image_delete_view(request, id=None):
    image = get_object_or_404(ProductImage, id=id, active=True)
    image.delete()
    messages.success(request, _("Image deleted successfully."))
    return redirect('product_image')






# PRODUCT VIEW 
@login_required
def product_view(request):
    products    = Product.objects.all()
    context = {
        'products': products,
    }
    template = "dashboard/product/product.html"
    return render(request, template, context)






# PRODUCT ADD VIEW 
@login_required
def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Produit créé avec succès."))
            return redirect('product')
    else:
        form = ProductForm()

    context = {'form': form}
    template = "dashboard/product/product-add.html"
    return render(request, template, context)




# PRODUCT DELETE VIEW

@login_required
def product_delete_view(request, slug=None):
    caregory = get_object_or_404(Product, slug=slug, active=True)
    caregory.delete()
    messages.success(request, _("Category deleted successfully."))
    return redirect('product')










# PRODUCT CATEGORY VIEW 
@login_required
def product_category_view(request):
    categories    = ProductCategory.objects.all()
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Category créé avec succès."))
            return redirect('product_category')
    else:
        form = ProductCategoryForm()
    context = {
        'categories': categories,
        'form': form
    }
    template = "dashboard/product/category.html"
    return render(request, template, context)







# PRODUCT CATEGORY DELETE

@login_required
def product_category_delete_view(request, slug=None):
    caregory = get_object_or_404(ProductCategory, slug=slug, active=True)
    caregory.delete()
    messages.success(request, _("Category deleted successfully."))
    return redirect('product_category')











# SUPPLIER VIEW 
@login_required
def supplier_view(request):
    suppliers    = Supplier.objects.all()
    context = {
        'suppliers': suppliers,
    }
    template = "dashboard/supplier/supplier.html"
    return render(request, template, context)









# SUPPLIER ADD VIEW 
@login_required
def supplier_add_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.created_by = request.user
            form.save()
            messages.success(request, _("Fournisseur créé avec succès."))
            return redirect('supplier')
    else:
        form = SupplierForm()

    context = {'form': form}
    template = "dashboard/supplier/supplier-add.html"
    return render(request, template, context)









# SUPPLIER DELETE VIEW

@login_required
def supplier_delete_view(request, slug=None):
    supplier = get_object_or_404(Supplier, slug=slug, active=True)
    supplier.delete()
    messages.success(request, _("Supplier deleted successfully."))
    return redirect('supplier')








# STOCK VIEW 
@login_required
def stock_view(request):
    stocks    = Supplier.objects.all()
    context = {
        'stocks': stocks,
    }
    template = "dashboard/stock/stock.html"
    return render(request, template, context)








# STOCK ADD VIEW 
@login_required
def stock_add_view(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.created_by = request.user
            form.save()
            messages.success(request, _("Stock créé avec succès."))
            return redirect('stock')
    else:
        form = StockForm()

    context = {'form': form}
    template = "dashboard/stock/stock-add.html"
    return render(request, template, context)







# STOCK DELETE VIEW

@login_required
def stock_delete_view(request, slug=None):
    stock = get_object_or_404(Stock, slug=slug, active=True)
    stock.delete()
    messages.success(request, _("Stock deleted successfully."))
    return redirect('stock')










# APPOINTMENT SYMPTOMS VIEW 
@login_required
def appointment_symptom_view(request):
    appointmentSymptoms    = AppointmentSymptom.objects.all()
    if request.method == 'POST':
        form = AppointmentSymptomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Symptoms Rendez-vous créé avec succès."))
            return redirect('appointment_symptom')
    else:
        form = AppointmentSymptomForm()
    context = {
        'appointmentSymptoms': appointmentSymptoms,
        'form': form
    }
    template = "dashboard/appointment/appointment-symptom.html"
    return render(request, template, context)









# APPOINTMENT SYMPTOMS DELETE VIEW 

@login_required
def appointment_symptom_delete_view(request, slug=None):
    appointmentSymptom = get_object_or_404(AppointmentSymptom, slug=slug, active=True)
    appointmentSymptom.delete()
    messages.success(request, _("Appointment Symptom deleted successfully."))
    return redirect('appointment_symptom')









# APPOINTMENT VIEW 
@login_required
def appointment_view(request):
    appointments    = Appointment.objects.all()
    context = {
        'appointments': appointments,
    }
    template = "dashboard/appointment/appointment.html"
    return render(request, template, context)










# APPOINTMENT ADD VIEW 
@login_required
def appointment_add_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Rendez-Vous créé avec succès."))
            return redirect('appointment')
    else:
        form = AppointmentForm()

    context = {'form': form}
    template = "dashboard/appointment/appointment-add.html"
    return render(request, template, context)










# APPOINTMENT DELETE VIEW

@login_required
def appointment_delete_view(request, slug=None):
    appointment = get_object_or_404(Appointment, slug=slug, active=True)
    appointment.delete()
    messages.success(request, _("Appointment  deleted successfully."))
    return redirect('appointment')










# APPOINTMENT PRESCRIPTION VIEW 
@login_required
def appointment_prescription_view(request):
    appointmentPrescriptions    = AppointmentPrescription.objects.all()
    context = {
        'appointmentPrescriptions': appointmentPrescriptions,
    }
    template = "dashboard/appointment/appointment-prescription.html"
    return render(request, template, context)









# APPOINTMENT PRESCRIPTION ADD VIEW 
@login_required
def appointment_prescription_add_view(request):
    if request.method == 'POST':
        form = AppointmentPrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Prescription Rendez-Vous créé avec succès."))
            return redirect('appointment_prescription')
    else:
        form = AppointmentPrescriptionForm()

    context = {'form': form}
    template = "dashboard/appointment/appointment-prescription-add.html"
    return render(request, template, context)






# APPOINTMENT PRESCRIPTION DELETE VIEW

@login_required
def appointment_prescription_delete_view(request, slug=None):
    appointment = get_object_or_404(AppointmentPrescription, slug=slug, active=True)
    appointment.delete()
    messages.success(request, _("Appointment  Prescription  deleted successfully."))
    return redirect('appointment_prescription')