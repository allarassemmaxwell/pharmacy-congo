# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.conf import settings

import uuid
from django.db import models
from django.db.models.fields import DateField
from django_countries.fields import CountryField
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core import validators

from django.urls import reverse



import random   
import string  
import secrets 





# GENERATE RANDOM STRING WITH LENGTH 
def random_string(num):   
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
    return str(res)








# CONTACT MODEL
class Contact(models.Model):
    first_name = models.CharField(_("Nom"), max_length=255, null=False, blank=False)
    last_name  = models.CharField(_("Prénom"), max_length=255, null=False, blank=False)
    email      = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    subject    = models.CharField(_("Suject"), max_length=255, null=False, blank=False)
    phone      = models.CharField(_("Téléphone"), max_length=255, null=False, blank=False)
    message    = models.TextField(_("Message"), null=False, blank=False)
    read       = models.BooleanField(_("Lu"), default=False)
    active     = models.BooleanField(_("Active"), default=True)
    timestamp  = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug       = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.email
    
    
    def delete_url(self):
        return reverse("contact_delete", args=[str(self.id)])

    def update_url(self):
        return reverse("contact_update", args=[str(self.id)])
    
    def respond_url(self):
        return reverse("contact_respond", args=[str(self.slug)])

    class Meta:
        ordering = ("-timestamp",)

def create_contact_slug(instance, new_slug=None):
    slug = slugify(random_string(14))
    if new_slug is not None:
        slug = new_slug
    ourQuery = Contact.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_contact_slug(instance, new_slug=new_slug)
    return slug

def presave_contact(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_contact_slug(instance)
pre_save.connect(presave_contact, sender=Contact)










# CONTACT MODEL
class ContactResponse(models.Model):
    contact   = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False, blank=False, related_name="contact_response")
    response  = models.TextField(_("Message"), null=False, blank=False)
    active    = models.BooleanField(_("Active"), default=True)
    timestamp = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated   = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug      = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.contact.email
    
    
    def delete_url(self):
        return reverse("contact_delete", args=[str(self.id)])

    def update_url(self):
        return reverse("contact_update", args=[str(self.id)])

    class Meta:
        ordering = ("-timestamp",)




def create_contact_response_slug(instance, new_slug=None):
    slug = slugify(random_string(14))
    if new_slug is not None:
        slug = new_slug
    ourQuery = ContactResponse.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_contact_response_slug(instance, new_slug=new_slug)
    return slug

def presave_contact_response(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_contact_response_slug(instance)
pre_save.connect(presave_contact_response, sender=ContactResponse)














# SUBSCRIBER MODEL
class Subscriber(models.Model):
    email      = models.EmailField(_("Email"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Active"), default=True)
    timestamp  = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email
    
    def delete_url(self):
        return reverse("newsletter_delete", args=[str(self.id)])

    def update_url(self):
        return reverse("newsletter_update", args=[str(self.id)])

    class Meta:
        ordering = ("-timestamp",)









# SUBSCRIBER MODEL
class EmailSubscriber(models.Model):
    name        = models.CharField(_("Sujet"), max_length=255, null=False, blank=False)
    description = models.TextField(_("Description"), null=False, blank=False)
    active      = models.BooleanField(_("Active"), default=True)
    timestamp   = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug        = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    def __str__(self):
        return self.name
    
    # def delete_url(self):
    #     return reverse("newsletter_delete", args=[str(self.id)])

    # def update_url(self):
    #     return reverse("newsletter_update", args=[str(self.id)])

    class Meta:
        ordering = ("-timestamp",)



def create_email_subs_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = EmailSubscriber.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_email_subs_slug(instance, new_slug=new_slug)
    return slug

def presave_email_subs(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_email_subs_slug(instance)
pre_save.connect(presave_email_subs, sender=EmailSubscriber)












# SUBSCRIBER RESPONSE MODEL
class SubscriberResponse(models.Model):
    subscriber   = models.ForeignKey(Subscriber, on_delete=models.CASCADE, null=False, blank=False, related_name="subscriber_response")
    subject  = models.TextField(_("Sujet"), null=False, blank=False)
    message  = models.TextField(_("Message"), null=False, blank=False)
    active    = models.BooleanField(_("Active"), default=True)
    timestamp = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated   = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug      = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.subscriber.email
    
    
    def delete_url(self):
        return reverse("subscriber_delete", args=[str(self.id)])

    def update_url(self):
        return reverse("subscriber_update", args=[str(self.id)])

    class Meta:
        ordering = ("-timestamp",)
















# BLOG CATEGORY MODEL
class BlogCategory(models.Model):
    name        = models.CharField(_("Name"), max_length=255, null=False, blank=False, unique=True)
    active      = models.BooleanField(_("Active"), default=True)
    timestamp   = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug        = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.name
    
    
    def delete_url(self):
        return reverse("blog_category_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("blog_category_update", args=[str(self.slug)])

    class Meta:
        ordering = ("-timestamp",)
    
    verbose_name_plural = _('BlogCategories')





def create_blog_cat_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = BlogCategory.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_blog_cat_slug(instance, new_slug=new_slug)
    return slug

def presave_blog_cat(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_blog_cat_slug(instance)
pre_save.connect(presave_blog_cat, sender=BlogCategory)











# BLOG MODEL
class Blog(models.Model):
    # user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    category    = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=False, blank=False, related_name="blog_category")
    name        = models.CharField(_("Name"), max_length=255, null=False, blank=False)
    photo       = models.ImageField(_("Image"), upload_to="Blog/%Y/%m/%d/", null=False, blank=False)
    description = models.TextField(_("Description"), null=False, blank=False)
    active      = models.BooleanField(_("Active"), default=True)
    timestamp   = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug        = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.name

    # GET ALERT DETAIL ABSOLUTE URL
    def get_detail_url(self):
        return reverse("landing:blog_detail", args=[str(self.slug)])
    
    def delete_url(self):
        return reverse("blog_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("blog_update", args=[str(self.slug)])


    class Meta:
        ordering = ("-timestamp",)



def create_blog_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Blog.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_blog_slug(instance, new_slug=new_slug)
    return slug

def presave_blog(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_blog_slug(instance)
pre_save.connect(presave_blog, sender=Blog)









# BLOG COMMENT MODEL
class BlogComment(models.Model):
	blog      = models.ForeignKey(Blog, on_delete=models.CASCADE, null=False, blank=False, related_name="comment_blog")
	name      = models.CharField(_("Name"), max_length=255, null=False, blank=False)
	email     = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
	comment   = models.TextField(_("Comment"), null=False, blank=False)
	active    = models.BooleanField(_("Active"), default=True)
	timestamp = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
	updated   = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ("-timestamp",)









# TESTIMONY MODEL
class Testimony(models.Model):
    full_name   = models.CharField(_("Full Name"), max_length=255, null=False, blank=False)
    image 		= models.ImageField(_("Image"), upload_to='Testimony/%Y/%m/', null=True, blank=True)
    occupation  = models.CharField(_("Occupation"), max_length=255, null=False, blank=False)
    description = models.TextField(_("Description"), null=False, blank=False)
    active 		= models.BooleanField(_("Status"), default=True)
    timestamp 	= models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated 	= models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.full_name
    
    def delete_url(self):
        return reverse("testimony_delete", args=[str(self.id)])

    def update_url(self):
        return reverse("testimony_update", args=[str(self.id)])


    class Meta:
        ordering = ('-timestamp',)
        verbose_name_plural = _('Testimonies')












# PARTNER MODEL
class Partner(models.Model):
    name 	     = models.CharField(_("Name"), max_length=255, null=False, blank=False)
    logo         = models.ImageField(_("Logo"), upload_to='Partner/%Y/%m/', null=False, blank=False)
    website      = models.URLField(_("Website URL"), max_length=255, null=True, blank=True)
    active 	     = models.BooleanField(_("Status"), default=True)
    timestamp    = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated      = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug         = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.name
    
    
    def delete_url(self):
        return reverse("partner_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("partner_update", args=[str(self.slug)])



    class Meta:
        ordering = ('-timestamp',)



def create_partner_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Partner.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_partner_slug(instance, new_slug=new_slug)
    return slug

def presave_partner(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_partner_slug(instance)
pre_save.connect(presave_partner, sender=Partner)


























