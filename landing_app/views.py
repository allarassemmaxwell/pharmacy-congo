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














# LANDING FUNCTION
def home_view(request):
	context  = {
	}
	template = "landing/base.html"
	return render(request, template, context)







# CONTACT VIEW 
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry" 
            body = {
                'first_name': form.cleaned_data['first_name'], 
                'last_name':  form.cleaned_data['last_name'], 
                'email':      form.cleaned_data['email'], 
                'message':    form.cleaned_data['message'], 
            }
            # message = "\n".join(body.values())
            # try:
            #     send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
            # except BadHeaderError:
            #     messages.error(request, _("Error. Message not sent."))
            form.save()
            messages.success(request, _("Your message has been sent successfully, we will get back to you as soon as possible."))
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = ContactForm()
    context  = {'form': form}
    template ="landing/contact.html"
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
    }
    template = "ecommerce/blog/blog.html"
    return render(request, template, context)





# BLOG DETAIL VIEW 
def blog_detail_view(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug, active=True)
    blog_categories = BlogCategory.objects.filter(active=True)
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
    }
    template ="landing/blog/blog-detail.html"
    return render(request, template, context)








# ABOUT VIEW  
def about_view(request):
    testimonies = Testimony.objects.filter(active=True) 
    context = {'testimonies':testimonies}
    template = "landing/about.html"
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





