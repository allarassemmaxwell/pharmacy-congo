from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import activate, gettext_lazy as _
from .forms import *
# from dashboard.forms import *
from .models import *
# from dashboard.models import *
from django.contrib import messages

from datetime import date, timedelta
import random
from django.http import HttpResponse

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator
from dashboard_app.models import *













# LANDING FUNCTION
def home_view(request):
	context  = {
	}
	template = "landing/index.html"
	return render(request, template, context)







# LANDING PHARMACY FUNCTION
def pharmacy_view(request):
	context  = {
	}
	template = "landing/pharmacy/pharmacy.html"
	return render(request, template, context)







	# CONTACT VIEW 
def contact_view(request):
	if request.method =='POST':
		form = ContactForme(request.POST)
		if form.is_valid():
			contact = form.save()
			subject = "Nouveau contact envoyé"
			Notification.objects.create(contact=contact, subject=subject)
			messages.success(request, "Votre message a été envoyé avec succés")
			return redirect(request.META['HTTP_REFERER'])
	else:
		form = ContactForme()
	context  = {'form':form}
	template ="contact.html"
	return render(request, template, context)











# BLOG VIEW 
def blog_view(request):
    category = ''
    blogs    = Blog.objects.filter(active=True)
    blog_categories = BlogCategory.objects.filter(active=True)
    category_slug = request.GET.get('category')

    if category_slug:
        blogs = Blog.objects.filter(category__slug=category_slug, active=True)

    # PAGINATION 
    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,
        'blog_categories': blog_categories,
        'category': category,
    }
    template = "landing/blog/blog.html"
    return render(request, template, context)





# BLOG DETAIL VIEW 
def blog_detail_view(request, slug=None):
	blog = get_object_or_404(Blog, slug=slug, active=True)
	blog_categories = BlogCategory.objects.filter(active=True)
	comments = BlogComment.objects.filter(active=True, blog=blog)
	recent_blogs    = Blog.objects.filter(active=True).exclude(slug=blog.slug)[:10]
	related_blogs   = Blog.objects.filter(active=True, category=blog.category).exclude(slug=blog.slug)[:10]
	if request.method == 'POST':
		form = BlogCommentForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.blog = blog
			form.save()
			messages.success(request, _("Comment posted successfully"))
		return redirect(request.META['HTTP_REFERER'])
	else:
		form = BlogCommentForm()
	context  = {
		'blog': blog,
		'form': form,
		'blog_categories': blog_categories,
		'recent_blogs': recent_blogs,
		'related_blogs': related_blogs,
		'comments': comments
	}
	template ="landing/blog/blog-detail.html"
	return render(request, template, context)








# ABOUT VIEW  
def about_view(request):
    testimonies = Testimony.objects.filter(active=True) 
    context = {'testimonies':testimonies}
    template = "about.html"
    return render(request,template,context)

    




# SUBSCRIBER VIEW FUNCTION 
def newsletter_view(request):
    email = request.POST.get('email')
    if Subscriber.objects.filter(email=email).exists():
        messages.error(request, _("You have already subscribed to our newsletter"))
        return redirect(request.META['HTTP_REFERER'])
    else:
        Subscriber.objects.create(email=email)
        messages.success(request, _("You have subscribed to our newsletter"))
        return redirect(request.META['HTTP_REFERER'])







#  PRODUCT FUNCTION
def product_view(request):
    category = ''
    products    = Product.objects.filter(active=True)
    names   = Product.objects.filter(active=True)
    product_categories = ProductCategory.objects.filter(active=True)
    category_slug = request.GET.get('category')

    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, active=True)

    # PAGINATION 
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
		'products': page_obj,
		'names': names,
		'product_categories': product_categories,
		'category': category,
	}
    
    template = "landing/pharmacy/product.html"
    return render(request, template, context)







#  PRODUCT FUNCTION
def product_list_view(request):
	context  = {
	}
	template = "landing/pharmacy/product-list.html"
	return render(request, template, context)





#  PRODUCT DETAILS FUNCTION
def product_detail_view(request):
	context  = {
	}
	template = "landing/pharmacy/product-detail.html"
	return render(request, template, context)







#  PHARMACY REGISTER FUNCTION
def pharmacy_register_view(request):
	context  = {
	}
	template = "landing/pharmacy/pharmacy-register.html"
	return render(request, template, context)










#  PHARMACY LOGIN FUNCTION
def pharmacy_login_view(request):
	context  = {
	}
	template = "landing/pharmacy/pharmacy-login.html"
	return render(request, template, context)








#  PHARMACY SEARCH FUNCTION
def pharmacy_search_view(request):
	context  = {
	}
	template = "landing/pharmacy/pharmacy-search.html"
	return render(request, template, context)










#  PHARMACY DETAIL FUNCTION
def pharmacy_detail_view(request):
	context  = {
	}
	template = "landing/pharmacy/pharmacy-detail.html"
	return render(request, template, context)












#################################################################
#                    PHARMACIST DASHBOARD
#################################################################


# PHARMACIST DASHBOARD FUNCTION
def pharmacist_dashboard_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/index.html"
	return render(request, template, context)







# PHARMACIST ADD PROFILE FUNCTION
def phcist_add_profile_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/phcist-add-profile.html"
	return render(request, template, context)








# PHARMACIST APPOINTMENT FUNCTION
def phcist_appointment_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/phcist-appointment.html"
	return render(request, template, context)









# PHARMACIST PATIENT FUNCTION
def phcist_patient_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/my-patient.html"
	return render(request, template, context)









# PHARMACIST PATIENT PROFILE FUNCTION
def phcist_patient_profile_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/phcist-patient-profile.html"
	return render(request, template, context)







# PHARMACIST ADD PRESCRIPTION FUNCTION
def add_prescription_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/add-prescription.html"
	return render(request, template, context)






# PHARMACIST ADD MEDICAL RECORD FUNCTION
def add_billing_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/add-billing.html"
	return render(request, template, context)







# PHARMACIST INVOICES FUNCTION
def phcist_invoice_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/phcist-invoice.html"
	return render(request, template, context)







# PHARMACIST SHOW INVOICES VIEW FUNCTION
def phcist_show_invoice_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/phcist-show-invoice.html"
	return render(request, template, context)







# PHARMACIST REGISTER VIEW FUNCTION
def phcist_register_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/phcist-register.html"
	return render(request, template, context)








# PHARMACIST LOGIN VIEW FUNCTION
def phcist_login_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/phcist-login.html"
	return render(request, template, context)






# PHARMACIST ADD BLOG VIEW FUNCTION
def phcist_add_blog_view(request):
	context  = {
	}
	template = "dashboard/pharmacist/phcist-add-blog.html"
	return render(request, template, context)







# PATIENT DASHBOARD FUNCTION
def patient_dashboard_view(request):
	context  = {
	}
	template = "dashboard/patient/index.html"
	return render(request, template, context)








# PATIENT SEARCH PHARMACIST FUNCTION
def search_pharmacist_view(request):
	context  = {
	}
	template = "dashboard/patient/search-pharmacist.html"
	return render(request, template, context)






# PATIENT  PHARMACIST PROFILE FUNCTION
def phcist_profile_view(request):
	context  = {
	}
	template = "dashboard/patient/phcist-profile.html"
	return render(request, template, context)







# PATIENT  CHECKOUT FUNCTION
def checkout_view(request):
	context  = {
	}
	template = "dashboard/patient/checkout.html"
	return render(request, template, context)







# PATIENT  BOOKING FUNCTION
def booking_view(request):
	context  = {
	}
	template = "dashboard/patient/booking.html"
	return render(request, template, context)









# PATIENT  FAVORITES FUNCTION
def favorite_pharmacist_view(request):
	context  = {
	}
	template = "dashboard/patient/favorite-pharmacist.html"
	return render(request, template, context)









# PATIENT  ADD PROFILE FUNCTION
def patient_add_profile_view(request):
	context  = {
	}
	template = "dashboard/patient/patient-add-profile.html"
	return render(request, template, context)








# PATIENT  CHANGE PASSWORD FUNCTION
def patient_change_password_view(request):
	context  = {
	}
	template = "dashboard/patient/patient-change-password.html"
	return render(request, template, context)







# PATIENT  FORGOT PASSWORD FUNCTION
def forgot_password_view(request):
	context  = {
	}
	template = "landing/pharmacy/forgot-password.html"
	return render(request, template, context)





# ADMIN PHARMACY

def pharmacy_admin_view(request):
    context = {
	}
    template = "dashboard/admin/pharmacy/index.html"
    return render(request,template, context)

