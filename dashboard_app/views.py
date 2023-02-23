from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import activate, gettext_lazy as _

# from .forms import *
from .models import *
# from .serializers import *
# from .utils import *
from django.utils import timezone

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






# BLOG ADD VIEW 
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








# BLOG  UPDATE VIEW

@login_required
def blog_update_view(request, slug=None):
    obj  = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Blog mis a jour avec succès.."))
            return redirect('blog')
    else:
        form = BlogForm(instance=obj)
    context = { 
        'form': form
    }
    template = "dashboard/blog/blog-update.html"
    return render(request, template, context)









# BLOG DELETE VIEW

@login_required
def blog_delete_view(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug, active=True)
    blog.delete()
    messages.success(request, _("Blog  deleted successfully."))
    return redirect('blog')









# BLOG CATEGORY VIEW 
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









# BLOG CATEGORY UPDATE VIEW

@login_required
def blog_category_update_view(request, slug=None):
    obj  = get_object_or_404(BlogCategory, slug=slug)
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Categories mis a jour avec succès.."))
            return redirect('blog_category')
    else:
        form = BlogCategoryForm(instance=obj)
    context = { 
        'form': form
    }
    template = "dashboard/blog/category-update.html"
    return render(request, template, context)











# BLOG CATEGORY DELETE VIEW

@login_required
def blog_category_delete_view(request, slug=None):
    category = get_object_or_404(BlogCategory, slug=slug, active=True)
    category.delete()
    messages.success(request, _("Blog Category deleted successfully."))
    return redirect('blog_category')








# CONTACT  VIEW 
@login_required
def contact_view(request):
    contacts    = Contact.objects.all()
    context = {'contacts': contacts}
    template = "dashboard/contact.html"
    return render(request, template, context)








# CONTACT  ADD VIEW 
@login_required
def contact_add_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Contact créé avec succès."))
            return redirect('contact')
    else:
        form = ContactForm()

    context = {'form': form}
    template = "dashboard/contact-add.html"
    return render(request, template, context)








# CONTACT UPDATE VIEW

@login_required
def contact_update_view(request, id):
    obj  = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Contact mis a jour avec succès.."))
            return redirect('contact')
    else:
        form = ContactForm(instance=obj)
    context = { 
        'form': form
    }
    template = "dashboard/contact-update.html"
    return render(request, template, context)








# CONTACT DELETE VIEW

@login_required
def contact_delete_view(request, id):
    contact = get_object_or_404(Contact, id=id, active=True)
    contact.delete()
    messages.success(request, _("Contact deleted successfully."))
    return redirect('contact')










# BLOG VIEW 
@login_required
def newsletter_view(request):
    newsletters    = Subscriber.objects.all()
    context = {'newsletters': newsletters}
    template = "dashboard/newsletter/newsletter.html"
    return render(request, template, context)





# BLOG NEWSLETTER ADD VIEW 
@login_required
def newsletter_add_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Newsletter créé avec succès."))
            return redirect('newsletter')
    else:
        form = NewsletterForm()

    context = {'form': form}
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
            messages.success(request, _("Abonné(e) mis a jour avec succès.."))
            return redirect('newsletter')
    else:
        form = NewsletterForm(instance=obj)
    context = { 
        'form': form
    }
    template = "dashboard/newsletter/newsletter-update.html"
    return render(request, template, context)









# NEWSLETTER DELETE VIEW

@login_required
def newsletter_delete_view(request, id):
    newsletter = get_object_or_404(Subscriber, id=id, active=True)
    newsletter.delete()
    messages.success(request, _("Subscriber deleted successfully."))
    return redirect('newsletter')








# BLOG PARTNER VIEW 
@login_required
def partner_view(request):
    partners    = Partner.objects.all()
    context = {'partners': partners}
    template = "dashboard/partner/partner.html"
    return render(request, template, context)





# BLOG PARTNER ADD VIEW 
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









# BLOG PARTNER UPDATE VIEW

@login_required
def partner_update_view(request, slug=None):
    obj  = get_object_or_404(Partner, slug=slug)
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Partenaire mis a jour avec succès.."))
            return redirect('partner')
    else:
        form = PartnerForm(instance=obj)
    context = { 
        'form': form
    }
    template = "dashboard/partner/partner-update.html"
    return render(request, template, context)









# PARTNER DELETE VIEW

@login_required
def partner_delete_view(request, slug=None):
    partner = get_object_or_404(Partner, slug=slug, active=True)
    partner.delete()
    messages.success(request, _("Partner deleted successfully."))
    return redirect('partner')






# BLOG TESTIMONY VIEW 
@login_required
def testimony_view(request):
    testimonies    = Testimony.objects.all()
    context = {'testimonies': testimonies}
    template = "dashboard/testimony/testimony.html"
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

    context = {'form': form}
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
            messages.success(request, _("Témoignage mis a jour avec succès.."))
            return redirect('testimony')
    else:
        form = TestimonyForm(instance=obj)
    context = { 
        'form': form
    }
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
    patients    = Patients.objects.all()
    context = {'patients': patients}
    template = "dashboard/patient/patient.html"
    return render(request, template, context)








# PATIENT ADD VIEW 
@login_required
def patient_add_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Patient créé avec succès."))
            return redirect('patient')
    else:
        form = PatientForm()

    context = {'form': form}
    template = "dashboard/patient/patient-add.html"
    return render(request, template, context)






# PATIENT UPDATE VIEW


@login_required
def patient_update_view(request, slug=None):
    obj  = get_object_or_404(Patients, slug=slug)
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Patient updated successfully."))
            return redirect('patient')
    else:
        form = PatientForm(instance=obj)
    context = { 
        'form': form
    }
    template = "dashboard/patient/patient-update.html"
    return render(request, template, context)







# PATIENT DELETE VIEW

@login_required
def patient_delete_view(request, slug=None):
    patient = get_object_or_404(Patients, slug=slug, active=True)
    patient.delete()
    messages.success(request, _("Patient deleted successfully."))
    return redirect('patient')










# USER VIEW 
@login_required
def user_view(request):
    users    = User.objects.all()
    context = {'users': users}
    template = "dashboard/user/user.html"
    return render(request, template, context)







# USER ADD VIEW

@login_required
def user_add_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        profile = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile.is_valid():
            user = form.save()
            profile = profile.save(commit=False)
            created_by = User.objects.get(email=request.user.email)
            profile.user = user
            profile.created_by = created_by
            profile.save()
            # Notification.objects.create(name="Cet utilisateur a ajouté  un utilisateur: %s %s"%(user.first_name, user.last_name), sender=request.user, user=user)
            messages.success(request, _("Utilisateur/Utilisatrice créé(e) avec succès."))
            return redirect('user')
    else:
        form = UserForm()
        profile = ProfileForm()
    context  = {
        'form': form,
        'profile': profile
    }
    template = "dashboard/user/user-add.html"
    return render(request, template, context)












# USER UPDATE VIEW

@login_required
def user_update_view(request, id=None):
    obj  = get_object_or_404(Profile, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=obj.user)
        profile = ProfileForm(request.POST, request.FILES, instance=obj)
        if form.is_valid() and profile.is_valid():
            # obj = form.save(commit=False)
            # email = form.cleaned_data['email']
            # check_email = User.objects.filter(email=email).exclude(id=id)
            # if check_email:
            #     print("==== CHECK EMAIL HERE =====")
            #     print(check_email)
                # messages.error(request, _("Utilisateur avec cet email existe déjà."))
                # return redirect(request.META['HTTP_REFERER'])
                # return redirect('utilisateur')
            form.save()
            profile.save()
            messages.success(request, _("Utilisateur/Utilisatrice modifié(e) avec succès."))
            return redirect('utilisateur')
    else:
        form = UserForm(instance=obj.user)
        profile = ProfileForm(instance=obj)
    context  = {
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
    # Notification.objects.create(name="Cet utilisateur a supprimé l'utilisateur: %s %s."%(user.first_name, user.last_name), sender=request.user, user=user)
    user.delete()
    messages.success(request, _("Utlisateur/Utilisatrice supprimé(e) avec succès."))
    return redirect('user')






# SERVICE VIEW 
@login_required
def service_view(request):
    services    = Service.objects.all()
    context = {
        'services': services,
    }
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

    context = {'form': form}
    template = "dashboard/service/service-add.html"
    return render(request, template, context)







# SERVICE DELETE VIEW

@login_required
def service_delete_view(request, slug=None):
    service = get_object_or_404(Service, slug=slug, active=True)
    service.delete()
    messages.success(request, _("Service deleted successfully."))
    return redirect('service')







@login_required
def service_update_view(request, slug=None):
    obj  = get_object_or_404(Service, slug=slug)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Service updated successfully."))
            return redirect('service')
    else:
        form = ServiceForm(instance=obj)
    context = { 
        'form': form
    }
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






@login_required
def service_category_update_view(request, slug=None):
    obj  = get_object_or_404(ServiceCategory, slug=slug)
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Category updated successfully."))
            return redirect('service_category')
    else:
        form = ServiceCategoryForm(instance=obj)
    context = { 
        'form': form
    }
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
    context = {
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
    messages.success(request, _("Image deleted successfully."))
    return redirect('product_image')






def product_image_update_view(request, slug=None):
    obj  = get_object_or_404(ProductImage, slug=slug)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Image updated successfully."))
            return redirect('product_image')
    else:
        form = ProductImageForm(instance=obj)
    image = obj.file
    context = { 
        'form': form,
        'image': image
    }
    template = "dashboard/product/image-update.html"
    return render(request, template, context)








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











# KEYWORD UPDATE VIEW FUNCTION
@login_required
def product_update_view(request, slug=None):
    obj  = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Product updated successfully."))
            return redirect('product')
    else:
        form = ProductForm(instance=obj)
    # image = obj.product_image.file
    context = { 
        'form': form,
        # 'image': image
    }
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














# KEYWORD UPDATE VIEW FUNCTION
@login_required
def product_category_update_view(request, slug=None):
    obj  = get_object_or_404(ProductCategory, slug=slug)
    form = ProductCategoryForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, _("Category updated successfully."))
        return redirect('product_category')
    context = { 
        'form': form
    }
    template = "dashboard/product/category-update.html"
    return render(request, template, context)








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
    supplier = get_object_or_404(Supplier, slug=slug)
    supplier.delete()
    messages.success(request, _("Supplier deleted successfully."))
    return redirect('supplier')









# KEYWORD UPDATE VIEW FUNCTION
@login_required
def supplier_update_view(request, slug=None):
    obj  = get_object_or_404(Supplier, slug=slug)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Fournisseur updated successfully."))
            return redirect('supplier')
    else:
        form = SupplierForm(instance=obj)
    context = { 
        'form': form,
    }
    template = "dashboard/supplier/supplier-update.html"
    return render(request, template, context)









# STOCK VIEW 
@login_required
def stock_view(request):
    stocks    = Stock.objects.all()
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
def stock_delete_view(request, id=None):
    stock = get_object_or_404(Stock, id=id)
    stock.delete()
    messages.success(request, _("Stock deleted successfully."))
    return redirect('stock')









# KEYWORD UPDATE VIEW FUNCTION
@login_required
def stock_update_view(request, id=None):
    obj  = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Stock updated successfully."))
            return redirect('stock')
    else:
        form = StockForm(instance=obj)
    context = { 
        'form': form,
    }
    template = "dashboard/stock/stock-update.html"
    return render(request, template, context)









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
    appointmentSymptom = get_object_or_404(AppointmentSymptom, slug=slug)
    appointmentSymptom.delete()
    messages.success(request, _("Appointment Symptom deleted successfully."))
    return redirect('appointment_symptom')










# KEYWORD UPDATE VIEW FUNCTION
@login_required
def appointment_symptom_update_view(request, slug=None):
    obj  = get_object_or_404(AppointmentSymptom, slug=slug)
    if request.method == 'POST':
        form = AppointmentSymptomForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Appointment Symptom updated successfully."))
            return redirect('appointment_symptom')
    else:
        form = AppointmentSymptomForm(instance=obj)
    context = { 
        'form': form,
    }
    template = "dashboard/appointment/appointment-symptom-update.html"
    return render(request, template, context)









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







# APPOINTMENT UPDATE VIEW FUNCTION
@login_required
def appointment_update_view(request, id):
    obj  = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Appointment Symptom updated successfully."))
            return redirect('appointment')
    else:
        form = AppointmentForm(instance=obj)
    context = { 
        'form': form,
    }
    template = "dashboard/appointment/appointment-update.html"
    return render(request, template, context)









# APPOINTMENT DELETE VIEW

@login_required
def appointment_delete_view(request, id=None):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    messages.success(request, _("Appointment deleted successfully."))
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






# APPOINTMENT PRESCRIPTION UPDATE VIEW FUNCTION
@login_required
def appointment_prescription_update_view(request, id):
    obj  = get_object_or_404(AppointmentPrescription, id=id)
    if request.method == 'POST':
        form = AppointmentPrescriptionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Appointment Prescription updated successfully."))
            return redirect('appointment_prescription')
    else:
        form = AppointmentPrescriptionForm(instance=obj)
    context = { 
        'form': form,
    }
    template = "dashboard/appointment/appointment-prescription-update.html"
    return render(request, template, context)








# APPOINTMENT PRESCRIPTION DELETE VIEW

@login_required
def appointment_prescription_delete_view(request, id):
    appointment = get_object_or_404(AppointmentPrescription, id=id, active=True)
    appointment.delete()
    messages.success(request, _("Appointment  Prescription  deleted successfully."))
    return redirect('appointment_prescription')










# SALE VIEWS

@login_required
def sale_view(request):
    sales    = Sale.objects.all()
    context = {
        'sales': sales,
    }
    template = "dashboard/sale/sale.html"
    return render(request, template, context)






# SALE ADD VIEW 
@login_required
def sale_add_view(request):
    if request.method == 'POST':
        form = SaleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Vente créé avec succès."))
            return redirect('sale')
    else:
        form = SaleForm()

    context = {'form': form}
    template = "dashboard/sale/sale-add.html"
    return render(request, template, context)







# SALE DELETE VIEW

@login_required
def sale_delete_view(request, id=None):
    sale = get_object_or_404(Sale, id=id)
    sale.delete()
    messages.success(request, _("Sale deleted successfully."))
    return redirect('sale')









# SALE UPDATE VIEW

@login_required
def sale_update_view(request, id):
    obj  = get_object_or_404(Sale, id=id)
    if request.method == 'POST':
        form = SaleForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Sale updated successfully."))
            return redirect('sale')
    else:
        form = SaleForm(instance=obj)
    context = { 
        'form': form
    }
    template = "dashboard/sale/sale-update.html"
    return render(request, template, context)







