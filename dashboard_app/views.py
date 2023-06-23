from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.translation import activate, gettext_lazy as _
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist

from django.forms import formset_factory

# from django.urls import reverse
from django.http import Http404
import csv
# from uuid import UUID

# for PDF
from .pdf import html2pdf
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
import os
from django.views.generic import View
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import Table
import tempfile
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
import re
import io
from urllib.parse import quote



import pdfkit
# config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")


from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from landing_app.models import *

from landing_app.models import *
from patient_app.forms import *
from .forms import *
from django.core.mail import send_mail, BadHeaderError
import calendar



#for the charts

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from django.db.models import Sum ,Count, F
from django.http import JsonResponse
from django.utils import timezone
from django.db.models.functions import TruncDay
from datetime import date, datetime, timedelta





class PasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')





def get_current_day():
    now = datetime.datetime.now()
    return now.strftime("%d")

def get_current_week():
    now = datetime.datetime.now()
    return now.strftime("%W")

def get_current_month():
    now = datetime.datetime.now()
    return now.strftime("%m")

def get_current_year():
    now = datetime.datetime.now()
    return now.strftime("%Y")







# ==================================================
#                     DASHBOARD VIEWS
# ==================================================
# DASHBOARD VIEW 
@login_required
def dashboard_view(request):
    this_year = datetime.now().year
    this_month = datetime.now().month
    if request.user.role == "Patient":
       return redirect('patient:home')
    else:
        doctor_count  = User.objects.filter(role="Docteur").count()
        patient_count = Patient.objects.filter(active=True).count()
        patients = Patient.objects.filter(active=True)[:10]
        doctors  = User.objects.filter(role="Docteur")[:10]
        prescriptions = AppointmentPrescription.objects.filter(active=True)[:10]
        appointment_count = Appointment.objects.filter(active=True).count()
        month_s_appointments = Appointment.objects.filter(date__year=this_year, date__month=this_month, active=True)
        revenu_count = 0
        for sale in Sale.objects.all():
            revenu_count += sale.total
        context = {
            'doctor_count': doctor_count,
            'patient_count': patient_count,
            'appointment_count': appointment_count,
            'revenu_count': revenu_count,
            'month_s_appointments': month_s_appointments,
            'patients': patients,
            'doctors': doctors,
            'prescriptions': prescriptions
        }
        #👆 I added the code above to make it work
        
    # this_year = datetime.datetime.now().year
    # this_month = datetime.datetime.now().month
    # if request.user.role == "Patient":
    #    return redirect('patient:home')
    # else:
    #     doctor_count  = User.objects.filter(role="Docteur").count()
    #     patient_count = Patient.objects.filter(active=True).count()
    #     patients = Patient.objects.filter(active=True)[:10]
    #     doctors  = User.objects.filter(role="Docteur")[:10]
    #     prescriptions = AppointmentPrescription.objects.filter(active=True)[:10]
    #     appointment_count = Appointment.objects.filter(active=True).count()
    #     month_s_appointments = Appointment.objects.filter(date__year=this_year, date__month=this_month, active=True)
    #     revenu_count = 0
    #     for sale in Sale.objects.all():
    #         revenu_count += sale.total
    #     context = {
    #         'doctor_count': doctor_count,
    #         'patient_count': patient_count,
    #         'appointment_count': appointment_count,
    #         'revenu_count': revenu_count,
    #         'month_s_appointments': month_s_appointments,
    #         'patients': patients,
    #         'doctors': doctors,
    #         'prescriptions': prescriptions
    #     }
        template = "dashboard/index.html"
        return render(request,template,context)
        

    




@login_required
def profile_view(request):
    obj  = get_object_or_404(Profile, user=request.user.id)
    if obj.photo:
        profile_photo = obj.photo.url
    else:
        profile_photo = ""
    if request.method == 'POST':
        profile_form  = PatientProfileForm(request.POST, request.FILES, instance=obj)
        user_form     = PatientUserUpdateForm(request.POST, instance=obj.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile modifié avec succès."))
            return redirect('profile')
    else:
        user_form    = PatientUserUpdateForm(instance=obj.user)
        profile_form = PatientProfileForm(instance=obj)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_photo': profile_photo
    }
    template = "dashboard/profile/profile.html"
    return render(request, template, context)





# BLOG VIEW 
@login_required
def blog_view(request):
    blogs    = Blog.objects.all()
    context  = {'blogs': blogs}
    template = "dashboard/blog/blog.html"
    return render(request, template, context)






# BLOG ADD VIEW 
@login_required
def blog_add_view(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.success(request, _("Blogue créé avec succès."))
            return redirect('blog')
    else:
        form = BlogForm()
    context  = {'form': form}
    template = "dashboard/blog/blog-add.html"
    return render(request, template, context)








# BLOG  UPDATE VIEW

@login_required
def blog_update_view(request, slug=None):
    obj  = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Blogue mis à jour avec succès..."))
            return redirect('blog')
    else:
        form = BlogForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/blog/blog-update.html"
    return render(request, template, context)









# BLOG DELETE VIEW

@login_required
def blog_delete_view(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug, active=True)
    blog.delete()
    messages.success(request, _("Blogue supprimé avec succès."))
    return redirect('blog')









# BLOG CATEGORY VIEW 
@login_required
def blog_category_view(request):
    categories = BlogCategory.objects.all()
    context    = {'categories': categories}
    template   = "dashboard/blog/category.html"
    return render(request, template, context)




# BLOG VIEW 
@login_required
def blog_category_add_view(request):
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Catégorie créée avec succès."))
            return redirect('blog_category')
    else:
        form = BlogCategoryForm()
    context  = {'form': form}
    template = "dashboard/blog/category-add.html"
    return render(request, template, context)









# BLOG CATEGORY UPDATE VIEW

@login_required
def blog_category_update_view(request, slug=None):
    obj  = get_object_or_404(BlogCategory, slug=slug)
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Catégorie mise à jour avec succès"))
            return redirect('blog_category')
    else:
        form = BlogCategoryForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/blog/category-update.html"
    return render(request, template, context)











# BLOG CATEGORY DELETE VIEW

@login_required
def blog_category_delete_view(request, slug=None):
    category = get_object_or_404(BlogCategory, slug=slug, active=True)
    category.delete()
    messages.success(request, _("Catégorie supprimée avec succès."))
    return redirect('blog_category')








# CONTACT  VIEW 
@login_required
def contact_view(request):
    contacts = Contact.objects.all()
    context  = {'contacts': contacts}
    template = "dashboard/contact.html"
    return render(request, template, context)















# CONTACT DELETE VIEW

@login_required
def contact_delete_view(request, id):
    contact = get_object_or_404(Contact, id=id, active=True)
    contact.delete()
    messages.success(request, _("Contact supprimé avec succès."))
    return redirect('contact')







# CONTACT  ADD VIEW 
@login_required
def contact_responde_view(request, slug=None):
    contact = get_object_or_404(Contact, slug=slug)
    contact.read = True
    contact.save()
    if request.method == 'POST':
        form = ContactResponseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.contact = contact
            email = form.cleaned_data.get("email")
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            send_mail(
                subject, message,
                'from@example.com', [email],
                fail_silently=False,
            )
            obj.save()
            messages.success(request, _("Contact repondu avec succès."))
            return redirect('contact')
    else:
        form = ContactResponseForm()
    context  = {
        'form': form,
        'contact': contact
    }
    template = "dashboard/contact-response-add.html"
    return render(request, template, context)









# CONTACT  VIEW 
@login_required
def response_contact_view(request):
    responses = ContactResponse.objects.all()
    context   = {'responses': responses}
    template  = "dashboard/contact-response.html"
    return render(request, template, context)












# BLOG VIEW 
@login_required
def newsletter_view(request):
    newsletters = Subscriber.objects.all()
    context     = {'newsletters': newsletters}
    template    = "dashboard/newsletter/newsletter.html"
    return render(request, template, context)





# BLOG NEWSLETTER ADD VIEW 
@login_required
def newsletter_add_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Email ajouté avec succès."))
            return redirect('newsletter')
    else:
        form = NewsletterForm()
    context  = {'form': form}
    template = "dashboard/newsletter/newsletter-add.html"
    return render(request, template, context)












# BLOG NEWSLETTER UPDATE VIEW

@login_required
def newsletter_update_view(request, id=None):
    obj  = get_object_or_404(Subscriber, id=id)
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Abonné(e) mis à jour avec succès.."))
            return redirect('newsletter')
    else:
        form = NewsletterForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/newsletter/newsletter-update.html"
    return render(request, template, context)









# NEWSLETTER DELETE VIEW

@login_required
def newsletter_delete_view(request, id):
    newsletter = get_object_or_404(Subscriber, id=id)
    newsletter.delete()
    messages.success(request, _("Abonné(e) supprimé(e) avec succès."))
    return redirect('newsletter')









# NEWSLETTER VIEW 
@login_required
def newsletter_email_view(request):
    emails   = EmailSubscriber.objects.all()
    context  = {'emails': emails}
    template = "dashboard/newsletter/email-subscriber.html"
    return render(request, template, context)





# BLOG NEWSLETTER ADD VIEW 
@login_required
def mail_newsletter_view(request):
    mails    = EmailSubscriber.objects.all()
    context  = {'mails': mails}
    template = "dashboard/newsletter/email-subscriber.html"
    return render(request, template, context)






# BLOG NEWSLETTER ADD VIEW 
@login_required
def mail_newsletter_add_view(request):
    if request.method == 'POST':
        form = EmailSubscriberForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            form.save()
            for subscriber in Subscriber.objects.filter(active=True):
                send_mail(
                    subject, description,
                    'from@example.com', [subscriber.email],
                    fail_silently=False,
                )
            messages.success(request, _("Email envoyé aux personnes avec succès."))
            return redirect('mail_newsletter')
    else:
        form = EmailSubscriberForm()
    context  = {'form': form}
    template = "dashboard/newsletter/email-subscriber-add.html"
    return render(request, template, context)










# BLOG PARTNER VIEW 
@login_required
def partner_view(request):
    partners = Partner.objects.all()
    context  = {'partners': partners}
    template = "dashboard/partner/partner.html"
    return render(request, template, context)





# BLOG PARTNER ADD VIEW 
@login_required
def partner_add_view(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Partenaire créé(e) avec succès."))
            return redirect('partner')
    else:
        form = PartnerForm()
    context  = {'form': form}
    template = "dashboard/partner/partner-add.html"
    return render(request, template, context)









# BLOG PARTNER UPDATE VIEW

@login_required
def partner_update_view(request, slug=None):
    obj  = get_object_or_404(Partner, slug=slug)
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Partenaire mis(e) a jour avec succès.."))
            return redirect('partner')
    else:
        form = PartnerForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/partner/partner-update.html"
    return render(request, template, context)









# PARTNER DELETE VIEW

@login_required
def partner_delete_view(request, slug=None):
    partner = get_object_or_404(Partner, slug=slug, active=True)
    partner.delete()
    messages.success(request, _("Partenaire supprimé(e) avec succès."))
    return redirect('partner')






# BLOG TESTIMONY VIEW 
@login_required
def testimony_view(request):
    testimonies = Testimony.objects.all()
    context     = {'testimonies': testimonies}
    template    = "dashboard/testimony/testimony.html"
    return render(request, template, context)







# BLOG TESTIMONY VIEW 
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
    context  = {'form': form}
    template = "dashboard/testimony/testimony-add.html"
    return render(request, template, context)









# BLOG TESTIMONY UPDATE VIEW

@login_required
def testimony_update_view(request, id=None):
    obj  = get_object_or_404(Testimony, id=id)
    if request.method == 'POST':
        form = TestimonyForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Témoignage mis à jour avec succès..."))
            return redirect('testimony')
    else:
        form = TestimonyForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/testimony/testimony-update.html"
    return render(request, template, context)









# TESTIMONY DELETE VIEW

@login_required
def testimony_delete_view(request, id):
    testimony = get_object_or_404(Testimony, id=id, active=True)
    testimony.delete()
    messages.success(request, _("Témoignage supprimé avec success."))
    return redirect('testimony')









# PATIENT  VIEW 
@login_required
def patient_view(request):
    patients = Patient.objects.all()
    context  = {'patients': patients}
    template = "dashboard/patient/patient.html"
    return render(request, template, context)








# PATIENT ADD VIEW 
@login_required
def patient_add_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.reg_no = random_string(10)
            patient.save()
            messages.success(request, _("Patient créé avec succès."))
            return redirect('patient')
    else:
        form = PatientForm()
    context  = {'form': form}
    template = "dashboard/patient/patient-add.html"
    return render(request, template, context)






# PATIENT UPDATE VIEW


@login_required
def patient_update_view(request, slug=None):
    user = None
    user_boolean = False
    obj  = get_object_or_404(Patient, slug=slug)
    if obj.user:
        user_boolean = True
        user = get_object_or_404(Profile, user=obj.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user)
        user_form = UserUpdateForm(request.POST, instance=obj.user)
        patient_form = PatientForm(request.POST, request.FILES, instance=obj)
        if not user_boolean and patient_form.is_valid():
            patient_form.save()
            messages.success(request, _("Patient(e) modifié(e) avec succès."))
            return redirect('patient')
        else:
            user_form.save()
            messages.success(request, _("Patient(e) modifié(e) avec succès."))
            return redirect('patient')
    else:
        user_form    = UserUpdateForm(instance=obj.user)
        profile_form = ProfileForm(request.POST, instance=user)
        profile      = PatientForm(instance=obj)
    context  = {
        'user_boolean': user_boolean,
        'user_form': user_form,
        'profile_form':profile_form,
        'patient_form': profile,
    }
    template = "dashboard/patient/patient-update.html"
    return render(request, template, context)








# PATIENT DELETE VIEW

@login_required
def patient_delete_view(request, slug=None):
    patient = get_object_or_404(Patient, slug=slug, active=True)
    patient.delete()
    messages.success(request, _("Patient(e) supprimé(e) avec succès."))
    return redirect('patient')




@login_required
def patient_user_delete_view(request, slug=None):
    patient = get_object_or_404(Patient, id=id, active=True)
    user    = patient.suer.id
    patient.delete()
    patient.save()
    user.delete()
    user.save()
    messages.success(request, _("Patient(e) supprimé(e) avec succès."))
    return redirect('patient')










# USER VIEW 
@login_required
def user_view(request):
    users    = User.objects.all()
    context  = {'users': users}
    template = "dashboard/user/user.html"
    return render(request, template, context)







# USER ADD VIEW

@login_required
def user_add_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        profile = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile.is_valid():
            user = form.save(commit=False)
            password   = "Log Support@#!1"
            user.set_password=password
            
            profile = profile.save(commit=False)

            profile.user = user
            user.save()
            profile.save()

            # email      = request.data['email']
            # subject    = "Enregistrement d'un compte"
            # message    = "Veuillez trouver ci-dessous votre mot de passe pour pouvoir accéder au compte.\nMot de passe: "+password
            email_to   = [user.email]
            # email_from = settings.EMAIL_HOST_USER
            # send_mail(subject, message, email_from, email_to, fail_silently=False,)


            messages.success(request, _("Utilisateur/Utilisatrice créé(e) avec succès."))
            return redirect('user')
    else:
        form    = UserForm()
        profile = ProfileForm()
    context     = {
        'form': form,
        'profile': profile
    }
    template = "dashboard/user/user-add.html"
    return render(request, template, context)












# USER UPDATE VIEW

@login_required
def user_update_view(request, id=None):
    obj  = get_object_or_404(Profile, user_id=id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=obj.user)
        profile = ProfileForm(request.POST, request.FILES, instance=obj)
        if form.is_valid() and profile.is_valid():
            form.save()
            profile.save()
            messages.success(request, _("Utilisateur/Utilisatrice modifié(e) avec succès."))
            return redirect('user')
    else:
        form    = UserUpdateForm(instance=obj.user)
        profile = ProfileForm(instance=obj)
    context     = {
        'form': form,
        'profile': profile,
        'photo': obj.photo
    }
    template = "dashboard/user/user-update.html"
    return render(request, template, context)










# USER DELETE VIEW

@login_required
def user_delete_view(request, id=None):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, _("Utlisateur/Utilisatrice supprimé(e) avec succès."))
    return redirect('user')






# SERVICE VIEW 
@login_required
def service_view(request):
    services = Service.objects.all()
    context  = {'services': services}
    template = "dashboard/service/service.html"
    return render(request, template, context)




# SERVICE ADD VIEW 
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
    context  = {'form': form}
    template = "dashboard/service/service-add.html"
    return render(request, template, context)







# SERVICE DELETE VIEW

@login_required
def service_delete_view(request, slug=None):
    service = get_object_or_404(Service, slug=slug, active=True)
    service.delete()
    messages.success(request, _("Service supprimé avec succès."))
    return redirect('service')







@login_required
def service_update_view(request, slug=None):
    obj  = get_object_or_404(Service, slug=slug)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Service mis à jour avec succès."))
            return redirect('service')
    else:
        form = ServiceForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/service/sercvice-update.html"
    return render(request, template, context)











# BLOG VIEW 
@login_required
def service_category_view(request):
    categories    = ServiceCategory.objects.all()
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Catégorie créée avec succès."))
            return redirect('service_category')
    else:
        form = ServiceCategoryForm()
    context  = {
        'categories': categories,
        'form': form
    }
    template = "dashboard/service/category.html"
    return render(request, template, context)







@login_required
def service_category_delete_view(request, slug=None):
    category = get_object_or_404(ServiceCategory, slug=slug, active=True)
    category.delete()
    messages.success(request, _("Catégorie supprimée avec succès."))
    return redirect('service_category')






@login_required
def service_category_update_view(request, slug=None):
    obj  = get_object_or_404(ServiceCategory, slug=slug)
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Catégorie mise à jour avec succès"))
            return redirect('service_category')
    else:
        form = ServiceCategoryForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/service/category-update.html"
    return render(request, template, context)






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
    context  = {
        'images': images,
        'form': form
    }
    template = "dashboard/product/image.html"
    return render(request, template, context)




# PRODUCT IMAGE DELETE

@login_required
def product_image_delete_view(request, slug=None):
    image = get_object_or_404(ProductImage, slug=slug, active=True)
    image.delete()
    messages.success(request, _("Image supprimée avec succès."))
    return redirect('product_image')






def product_image_update_view(request, slug=None):
    obj  = get_object_or_404(ProductImage, slug=slug)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Image mise à jour avec succès."))
            return redirect('product_image')
    else:
        form = ProductImageForm(instance=obj)
    image    = obj.file
    context  = { 
        'form': form,
        'image': image
    }
    template = "dashboard/product/image-update.html"
    return render(request, template, context)








# PRODUCT VIEW 
@login_required
def product_view(request):
    products = Product.objects.all()
    context  = {'products': products}
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
    context  = {'form': form}
    template = "dashboard/product/product-add.html"
    return render(request, template, context)






# PRODUCT DELETE VIEW

@login_required
def product_delete_view(request, slug=None):
    caregory = get_object_or_404(Product, slug=slug, active=True)
    caregory.delete()
    messages.success(request, _("Produit supprimé avec succès."))
    return redirect('product')











# KEYWORD UPDATE VIEW FUNCTION
@login_required
def product_update_view(request, slug=None):
    obj  = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Produit mis à jour avec succès."))
            return redirect('product')
    else:
        form = ProductForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/product/product-update.html"
    return render(request, template, context)










# PRODUCT CATEGORY VIEW 
@login_required
def product_category_view(request):
    categories    = ProductCategory.objects.all()
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Catégorie créée avec succès."))
            return redirect('product_category')
    else:
        form = ProductCategoryForm()
    context  = {
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
    messages.success(request, _("Catégorie supprimée avec succès."))
    return redirect('product_category')














# KEYWORD UPDATE VIEW FUNCTION
@login_required
def product_category_update_view(request, slug=None):
    obj  = get_object_or_404(ProductCategory, slug=slug)
    form = ProductCategoryForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, _("Catégorie mise à jour avec succès."))
        return redirect('product_category')
    context = {'form': form}
    template = "dashboard/product/category-update.html"
    return render(request, template, context)








# SUPPLIER VIEW 
@login_required
def supplier_view(request):
    suppliers = Supplier.objects.all()
    context   = {'suppliers': suppliers}
    template  = "dashboard/supplier/supplier.html"
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
    context  = {'form': form}
    template = "dashboard/supplier/supplier-add.html"
    return render(request, template, context)









# SUPPLIER DELETE VIEW

@login_required
def supplier_delete_view(request, slug=None):
    supplier = get_object_or_404(Supplier, slug=slug)
    supplier.delete()
    messages.success(request, _("Fournisseur supprimé avec succès."))
    return redirect('supplier')









# KEYWORD UPDATE VIEW FUNCTION
@login_required
def supplier_update_view(request, slug=None):
    obj  = get_object_or_404(Supplier, slug=slug)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Fournisseur mis à jour avec succès."))
            return redirect('supplier')
    else:
        form = SupplierForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/supplier/supplier-update.html"
    return render(request, template, context)








# STOCK CATEGORY VIEW 
@login_required
def stock_category_view(request):
    categories    = StockCategory.objects.all()
    if request.method == 'POST':
        form = StockCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Catégorie créée avec succès."))
            return redirect('stock_category')
    else:
        form = StockCategoryForm()
    context  = {
        'categories': categories,
        'form': form
    }
    template = "dashboard/stock/category_stock.html"
    return render(request, template, context)










# STOCK CATEGORY DELETE

@login_required
def stock_category_delete_view(request, slug=None):
    caregory = get_object_or_404(StockCategory, slug=slug, active=True)
    caregory.delete()
    messages.success(request, _("Catégorie supprimée avec succès."))
    return redirect('stock_category')







# STOCK KEYWORD UPDATE VIEW FUNCTION
@login_required
def stock_category_update_view(request, slug=None):
    obj  = get_object_or_404(StockCategory, slug=slug)
    form = StockCategoryForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, _("Catégorie mise à jour avec succès."))
        return redirect('stock_category')
    context = {'form': form}
    template = "dashboard/stock/category-update.html"
    return render(request, template, context)















# STOCK VIEW 
@login_required
def stock_view(request):
    stocks  = Stock.objects.all()
    form    = StockSearchForm(request.POST or None)
    context = {
        'stocks': stocks,
        'form': form,
    }
    
    if request.method == 'POST':
        category  = form['category'].value()
        item_name = form['item_name'].value()
        stocks    = Stock.objects.filter(category__name__icontains=category, item_name__icontains=item_name)
        context['stocks'] = stocks

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Liste de stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['Catégorie', 'Nom Produit', 'Quantité en Stock'])
            for stock in stocks:
                writer.writerow([stock.category.name, stock.item_name, stock.quantity])
            return response
    
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
            obj = form.save(commit=False)
            obj.total = obj.unity_price * obj.quantity
            # obj.save()
            form.save()
            messages.success(request, _("Stock créé avec succès."))
            return redirect('stock')
    else:
        form = StockForm()
    context  = {'form': form}
    template = "dashboard/stock/stock-add.html"
    return render(request, template, context)









# STOCK DELETE VIEW

@login_required
def stock_delete_view(request, id=None):
    stock = get_object_or_404(Stock, id=id)
    stock.delete()
    messages.success(request, _("Stock supprimé avec succès."))
    return redirect('stock')









# KEYWORD UPDATE VIEW FUNCTION
@login_required
def stock_update_view(request, id=None):
    obj  = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.total = obj.unity_price * obj.quantity
            form.save()
            messages.success(request, _("Stock mis à jour avec succès."))
            return redirect('stock')
    else:
        form = StockForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/stock/stock-update.html"
    return render(request, template, context)







# STOCK DETAILS ITEMS

# 👉 detail items#
@login_required
def stock_detail_view(request, id):
    stocks = Stock.objects.get(id=id)
    context = {
        "stocks": stocks,
    }
    template = "dashboard/stock/stock_detail.html"
    return render(request, template, context)











# ISSUE ITEMS
# 👉 issue items (move out)
@login_required
def issue_items_view(request, id):
    stocks = Stock.objects.get(id=id)
    form = IssueForm(request.POST or None, instance=stocks)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        update_total   = instance.unity_price * instance.quantity
        instance.total = update_total

        messages.success(request, "Produit Délivré avec succès. " + str(instance.quantity) + " " + str(instance.item_name) + " stocké au magasin")
        instance.save()

        return redirect('stock_detail', id=instance.id)

    context = {
        "title": 'Issue ' + str(stocks.item_name),
        "stocks": stocks,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }

    template = "dashboard/stock/add_issue.html"
    return render(request, template, context)
    # return render(request, "add_items.html", context)
















#  RECEIVE ITEMS

# 👉 receive items
@login_required
def receive_items_view(request, id):
    stocks = get_object_or_404(Stock, id=id)
    form   = ReceiveForm(request.POST or None, instance=stocks)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        update_total   = instance.unity_price * instance.quantity
        instance.total = update_total
        instance.save()


        messages.success(request, f"Reçu avec succès. {instance.quantity} {instance.item_name} stocké au magasin")
        return redirect('stock_detail', id=instance.id)

    context = {
        "stocks": stocks,
        "form": form,
        "username": f"Reçu Par: {request.user}",
    }
    template = "dashboard/stock/add_receive.html"
    return render(request, template, context)













# 👉 reorder items
@login_required
def reorder_level_view(request, id):
    stocks = Stock.objects.get(id=id)
    form = ReorderLevelForm(request.POST or None, instance=stocks)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Niveau de réapprovisionnement pour " + str(stocks.item_name) + " est mis à jour à " + str(stocks.reorder_level))
        return redirect("stock")
    
    context = {
        "stocks": stocks,
        "form": form,
    }
    template = "dashboard/stock/add_reorder.html"
    return render(request, template, context)

















# APPOINTMENT SYMPTOMS VIEW 
@login_required
def appointment_symptom_view(request):
    appointmentSymptoms    = AppointmentSymptom.objects.all()
    if request.method == 'POST':
        form = AppointmentSymptomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Symptoms créé avec succès."))
            return redirect('appointment_symptom')
    else:
        form = AppointmentSymptomForm()
    context  = {
        'appointmentSymptoms': appointmentSymptoms,
        'form': form
    }
    template = "dashboard/appointment/appointment-symptom.html"
    return render(request, template, context)









# APPOINTMENT SYMPTOMS DELETE VIEW 

@login_required
def appointment_symptom_delete_view(request, slug=None):
    appointmentSymptom = get_object_or_404(AppointmentSymptom, slug=slug)
    appointmentSymptom.delete()
    messages.success(request, _("Symptôme supprimé avec succès."))
    return redirect('appointment_symptom')










# KEYWORD UPDATE VIEW FUNCTION
@login_required
def appointment_symptom_update_view(request, slug=None):
    obj  = get_object_or_404(AppointmentSymptom, slug=slug)
    if request.method == 'POST':
        form = AppointmentSymptomForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Symptôme mis à jour avec succès."))
            return redirect('appointment_symptom')
    else:
        form = AppointmentSymptomForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/appointment/appointment-symptom-update.html"
    return render(request, template, context)









# APPOINTMENT VIEW 
@login_required
def appointment_view(request):
    appointments = Appointment.objects.all()
    context      = {'appointments': appointments}
    template     = "dashboard/appointment/appointment.html"
    return render(request, template, context)










# APPOINTMENT ADD VIEW 
@login_required
def appointment_add_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get("date")
            hour = form.cleaned_data.get("hour")
            appointment = form.save()
            subject = "Nouveau rendez-vous le "+str(date)+" à "+str(hour)
            Notificaty.objects.create(appointment=appointment, subject=subject)
            messages.success(request, _("Rendez-Vous créé avec succès."))
            return redirect('appointment')
    else:
        form = AppointmentForm()
    context  = {
        'form': form
    }
    template = "dashboard/appointment/appointment-add.html"
    return render(request, template, context)







# APPOINTMENT UPDATE VIEW FUNCTION
@login_required
def appointment_update_view(request, id):
    obj  = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Rendez-vous Symptôme mis à jour avec succès."))
            return redirect('appointment')
    else:
        form = AppointmentForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/appointment/appointment-update.html"
    return render(request, template, context)









# APPOINTMENT DELETE VIEW

@login_required
def appointment_delete_view(request, id=None):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    messages.success(request, _("Rendez-vous supprimé avec succès."))
    if request.user.role == "Patient":
       return redirect('patient:appointment')
    else:
        return redirect('appointment')







# APPOINTMENT VIEW 
@login_required
def appointment_detail_view(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.read = True
    appointment.save()
    context  = {'appointment': appointment}
    template = "dashboard/appointment/appointment-detail.html"
    return render(request, template, context)







# APPOINTMENT PRESCRIPTION VIEW 
@login_required
def appointment_prescription_view(request):
    appointmentPrescriptions    = AppointmentPrescription.objects.all()
    context  = {'appointmentPrescriptions': appointmentPrescriptions}
    template = "dashboard/appointment/appointment-prescription.html"
    return render(request, template, context)









# APPOINTMENT PRESCRIPTION ADD VIEW 
@login_required
def appointment_prescription_add_view(request):
    if request.method == 'POST':
        form = AppointmentPrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Prescription créé avec succès."))
            return redirect('appointment_prescription')
    else:
        form = AppointmentPrescriptionForm()
    context  = {'form': form}
    template = "dashboard/appointment/appointment-prescription-add.html"
    return render(request, template, context)






# APPOINTMENT PRESCRIPTION UPDATE VIEW FUNCTION
@login_required
def appointment_prescription_update_view(request, id):
    obj  = get_object_or_404(AppointmentPrescription, id=id)
    if request.method == 'POST':
        form = AppointmentPrescriptionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Prescription mise à jour avec succès."))
            return redirect('appointment_prescription')
    else:
        form = AppointmentPrescriptionForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/appointment/appointment-prescription-update.html"
    return render(request, template, context)








# APPOINTMENT PRESCRIPTION DELETE VIEW

@login_required
def appointment_prescription_delete_view(request, id):
    appointment = get_object_or_404(AppointmentPrescription, id=id, active=True)
    appointment.delete()
    messages.success(request, _("Prescription supprimée avec succès."))
    return redirect('appointment_prescription')










# SALE VIEWS

@login_required
def sale_view(request):
    sales    = Sale.objects.all()
    context  = {'sales': sales}
    template = "dashboard/sale/sale.html"
    return render(request, template, context)






# SALE ADD VIEW
@login_required
def sale_add_view(request):
    SaleFormSet = formset_factory(SaleForm, extra=1)

    if request.method == 'POST':
        form = SaleForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.reference = random_string(7)
            obj.seller = request.user
            obj.total  = Decimal(obj.product.unity_price * obj.quantity)
            if obj.invoice_type == "Facture":
                print("======= ADD YOUR FACTURE FUNCTION HERE =======")
            elif obj.invoice_type == "Reçu":
                print("======= ADD YOUR RECU FUNCTION HERE ======= ")
            obj.save()
            messages.success(request, _("Vente créée avec succès."))
            return redirect('sale')
    else:
        formset = SaleFormSet(prefix='sales')

    context = {'formset': formset}
    template = "dashboard/sale/sale-add.html"
    return render(request, template, context)







# SALE DELETE VIEW

@login_required
def sale_delete_view(request, id=None):
    sale = get_object_or_404(Sale, id=id)
    sale.delete()
    messages.success(request, _("Vente supprimée avec succès."))
    return redirect('sale')









# SALE UPDATE VIEW

@login_required
def sale_update_view(request, id):
    obj  = get_object_or_404(Sale, id=id)
    if request.method == 'POST':
        form = SaleForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.total  = Decimal(obj.product.unity_price * obj.quantity)
            if obj.invoice_type == "Facture":
                print("======= ADD YOUR FACTURE FUNCTION HERE =======")
            elif obj.invoice_type == "Reçu":
                print("======= ADD YOUR RECU FUNCTION HERE ======= ")
            obj.save()
            messages.success(request, _("Vente mise à jour avec succès."))
            return redirect('sale')
    else:
        form = SaleForm(instance=obj)
    context  = {'form': form}
    template = "dashboard/sale/sale-update.html"
    return render(request, template, context)










# NOTIFICATION   FUNCTION
@login_required
def notification_view(request):
    notifications = Notificaty.objects.filter(active=True)
    context  = {'notifications': notifications}
    template = "dashboard/notification/notification.html"
    return render(request, template, context)
















# FRIDGE VIEW 
@login_required
def fridge_view(request):
    fridges = Fridge.objects.all()
    context  = {'fridges': fridges}
    template = "dashboard/fridge/fridge.html"
    return render(request, template, context)






# FRIDGE ADD VIEW 
@login_required
def fridge_add_view(request):
    if request.method == 'POST':
        form = FridgeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Frigidaire créé avec succès."))
            return redirect('fridge')
    else:
        form = FridgeForm()
    context  = {'form': form}
    template = "dashboard/fridge/fridge-add.html"
    return render(request, template, context)






# FRIDGE DELETE VIEW

@login_required
def fridge_delete_view(request, id):
    marque = get_object_or_404(Fridge, id=id, active=True)
    marque.delete()
    messages.success(request, _("Frigidaire supprimé avec succès."))
    return redirect('fridge')











# FRIDGE UPDATE VIEW FUNCTION
@login_required
def fridge_update_view(request, id):
    obj  = get_object_or_404(Fridge, id=id)
    if request.method == 'POST':
        form = FridgeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Frigidaire mis à jour avec succès."))
            return redirect('fridge')
    else:
        form = FridgeForm(instance=obj)
    # image  = obj.product_image.file
    context  = { 
        'form': form,
        # 'image': image
    }
    template = "dashboard/fridge/fridge-update.html"
    return render(request, template, context)












# INVOICE MANAGEMENT

# INVOICE VIEW 
@login_required
def invoice_view(request):
    invoices = Invoice.objects.all()
    context  = {'invoices': invoices}
    template = "dashboard/invoices/invoice.html"
    return render(request, template, context)









# SHOW INVOICE VIEW 
@login_required
def show_invoice_view(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    context = {'invoice': invoice}
    template = "dashboard/invoices/invoice_pdf.html"
    return render(request, template, context)












# INVOICE ADD VIEW 
@login_required
def invoice_add_view(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(commit=False)

            # Calculate the total
            total = Decimal(invoice.unity_price * invoice.quantity)
            invoice.total = total
            # Save the object
            form.save()

            messages.success(request, _("Facture créée avec succès."))
            return redirect('invoice')
    else:
        form = InvoiceForm()

    context = {'form': form}
    template = "dashboard/invoices/invoice-add.html"
    return render(request, template, context)












# INVOICE DELETE VIEW

@login_required
def invoice_delete_view(request, id):
    invoice = get_object_or_404(Invoice, id=id, active=True)
    invoice.delete()
    messages.success(request, _("Facture supprimée avec succès."))
    return redirect('invoice')











# INVOICE UPDATE VIEW FUNCTION
@login_required
def invoice_update_view(request, id):
    obj  = get_object_or_404(Invoice, id=id)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Facture mis à jour avec succès."))
            return redirect('invoice')
    else:
        form = InvoiceForm(instance=obj)
    # image  = obj.product_image.file
    context  = { 
        'form': form,
        # 'image': image
    }
    template = "dashboard/invoices/invoice-update.html"
    return render(request, template, context)




















# 👉 to generate pdf

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        invoice = get_object_or_404(Invoice, id=id)

        context = {
            'invoice': invoice
        }

        pdf = html2pdf('dashboard/invoices/invoice_pdf.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        customer_name = invoice.customer_name.replace(" ", "_")  # Replace spaces with underscores
        response['Content-Disposition'] = f'inline; filename="{customer_name}.pdf"'  # Use 'inline' instead of 'attachment'
        return response


# def invoice_pdf_view(request, id):
#     invoice = get_object_or_404(Invoice, id=id)
#     context = {'invoice': invoice}
#     template_name = 'dashboard/invoices/invoice_pdf.html'

#     html = render_to_string(template_name, context, request=request)
#     pdf_data = pisa.CreatePDF(html)

#     if pdf_data:
#         response = HttpResponse(content_type='application/pdf')
#         invoice_name = slugify(invoice.customer_name)
#         filename = f"invoice_{invoice_name}.pdf"
#         response['Content-Disposition'] = 'attachment; filename="{}"'.format(quote(filename))
#         response.write(pdf_data)
#         return response

#     return HttpResponse("Error generating PDF", status=500)










    # invoice = get_object_or_404(Invoice, id=id)
    # context = {'invoice': invoice}

    # html = render_to_string('dashboard/invoices/invoice_pdf.html', context)
    # pdf_data = html2pdf('dashboard/invoices/invoice_pdf.html', context)

    # if pdf_data is not None:
    #     response = HttpResponse(content_type='application/pdf')
    #     invoice_name = invoice[0].customer_name  # Assuming item_name is an attribute of Stock model
    #     filename = f"invoice_{invoice_name}.pdf"
    #     response['Content-Disposition'] = f'filename="{filename}"'
    #     response.write(pdf_data)
    #     return response

    # return HttpResponse("Error generating PDF", status=500)








































# Pages des Rapports de l'Entreprise

# RAPPORT QUOTIDIEN

# Page Rapport quotidien

@login_required
def rapport_quotidien_view(request):
     # Get the date from the request parameters or use the current date
    year = timezone.now().year
    month = timezone.now().month
    day = timezone.now().day
    
    if 'day' in request.GET and request.GET['day']:
        selected_date = request.GET['day']
        try:
            day, month, year = map(int, selected_date.split("-"))
        except ValueError:
            pass

    # Filter the sales for the selected day
    sales = Sale.objects.filter(timestamp__year=year, timestamp__month=month, timestamp__day=day, active=True)

    # Calculate the total amount and the sales for each product
    total_amount = sales.aggregate(Sum('total'))['total__sum'] or 0
    products_sales = sales.values('product__name').annotate(sales=Sum('total')).order_by('product__name')

    # Prepare the data for the chart
    chart_labels = [data['product__name'] for data in products_sales]
    chart_data = [float(data['sales']) for data in products_sales]

    context = {
        'sales': sales,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'total_amount': total_amount,
        'products_sales': products_sales,
    }
    
    template = "dashboard/report/quotidien.html"
    return render(request, template, context)








# RAPPORT HEBDOMADAIRE

# Page Rapport Hebdomadaire

@login_required
def rapport_hebdomadaire_view(request):
    # Get the week number from the request parameters or use the current week
    selected_date = request.GET.get('week', None)
    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%d-%m-%Y')
            week_number = selected_date_obj.isocalendar()[1]
        except ValueError:
            pass
    else:
        today = timezone.now()
        week_number = today.strftime('%V')

    # Filter the sales for the selected week
    sales = Sale.objects.filter(
        timestamp__week=week_number,
        active=True
    )

    # Calculate the total amount and the sales for each product
    total_amount = sales.aggregate(Sum('total'))['total__sum'] or 0
    products_sales = sales.values('product__name').annotate(sales=Sum('total')).order_by('product__name')

    # Prepare the data for the chart
    chart_labels = [data['product__name'] for data in products_sales]
    chart_data = [float(data['sales']) for data in products_sales]

    context = {
        'sales': sales,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'total_amount': total_amount,
        'products_sales': products_sales,
    }
    
    template = "dashboard/report/hebdomadaire.html"
    return render(request, template, context)















# RAPPORT MENSUEL

# Page de Rapport Mensuel

@login_required
def rapport_mensuel_view(request):
    date_string = request.GET.get('month')
    if date_string and len(date_string) == 7:
        # If only month and year are provided, use 1st day of month
        date_obj = datetime.strptime(date_string, "%m-%Y").date()
        first_day = date(date_obj.year, date_obj.month, 1)
        last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
        last_day = date(date_obj.year, date_obj.month, last_day)
    elif date_string is not None:
        # If full date is provided, use that date
        date_obj = datetime.strptime(date_string, "%d-%m-%Y").date()
        # Extract month and year from the provided date
        first_day = date(date_obj.year, date_obj.month, 1)
        last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
        last_day = date(date_obj.year, date_obj.month, last_day)
    else:
        # If no date string is provided, use the current month and year
        date_obj = timezone.now().date()
        first_day = date(date_obj.year, date_obj.month, 1)
        last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
        last_day = date(date_obj.year, date_obj.month, last_day)

    # Filter the sales for the selected month
    sales = Sale.objects.filter(timestamp__range=[first_day, last_day], active=True)

    # Calculate the total amount and the sales for each product
    total_amount   = sales.aggregate(Sum('total'))['total__sum'] or 0
    products_sales = sales.values('product__name').annotate(sales=Sum('total')).order_by('product__name')

    # Prepare the data for the chart
    chart_labels = [data['product__name'] for data in products_sales]
    chart_data   = [float(data['sales']) for data in products_sales]

    context = {
        'sales': sales,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'total_amount': total_amount,
        'products_sales': products_sales,
    }
    
    template = "dashboard/report/mensuel.html"
    return render(request, template, context)









# RAPPORT ANNUEL

# Page de Rapport annuel

@login_required
def rapport_annuel_view(request):
    year_str = request.GET.get('year', timezone.now().strftime('%d-%m-%Y'))
    try:
        year = datetime.strptime(year_str, '%d-%m-%Y').date().year
    except ValueError:
        # handle invalid year format
        year = timezone.now().year

    # Get the first and last day of the year
    first_day = date(year, 1, 1)
    last_day = date(year, 12, 31)

    # Filter the sales for the selected year
    sales = Sale.objects.filter(timestamp__range=[first_day, last_day], active=True)

    # Calculate the total amount and the sales for each product
    total_amount = sales.aggregate(Sum('total'))['total__sum'] or 0
    products_sales = sales.values('product__name').annotate(sales=Sum('total')).order_by('product__name')

    # Prepare the data for the chart
    chart_labels = [data['product__name'] for data in products_sales]
    chart_data = [float(data['sales']) for data in products_sales]

    context = {
        'sales': sales,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'total_amount': total_amount,
        'products_sales': products_sales,
    }


    template = "dashboard/report/annuel.html"
    return render(request, template, context)






















# GLOBAL  NOTIFICATION FUNCTION
def global_notification_view(request):
    notifications=[]
    for notification in Notificaty.objects.all():
        if notification.contact and notification.contact.read == False or notification.appointment and notification.appointment.read == False:
            notifications.append(notification)
    return {'GLOBAL_NOTIFICATIONS': notifications}






from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
# =========================================================
#                         PRODUCT 
# =========================================================

@api_view(['GET'])
# @permission_classes([IsAuthenticated, ])
def productList(request):
    if request.method == 'GET':
        data = Product.objects.filter(active=True)
        serializer = ProductSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)



