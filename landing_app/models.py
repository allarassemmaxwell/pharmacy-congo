# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.conf import settings

import uuid
from django.db import models
from django.db.models.fields import DateField
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core import validators

from django.urls import reverse










# CONTACT MODEL
class Contact(models.Model):
    first_name = models.CharField(_("First Name"), max_length=255, null=False, blank=False)
    last_name  = models.CharField(_("Last Name"), max_length=255, null=False, blank=False)
    email      = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    subject    = models.CharField(_("Subject"), max_length=255, null=False, blank=False)
    phone      = models.CharField(_("Phone"), max_length=255, null=False, blank=False)
    message    = models.TextField(_("Message"), null=False, blank=False)
    active     = models.BooleanField(_("Active"), default=True)
    timestamp  = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("-timestamp",)













# SUBSCRIBER MODEL
class Subscriber(models.Model):
    email      = models.EmailField(_("Email"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Active"), default=True)
    timestamp  = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email

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
	website   = models.URLField(_("Website"), max_length=255, null=True, blank=True)
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



    class Meta:
        ordering = ('-timestamp',)





# PATIENT MODEL
class Patients(models.Model):
    STATUS_CHOICES=(
        ('Masculin','Masculin'),
        ('Feminin','Feminin'),
    )
    # admin          = models.OneToOneField(User,null=True, on_delete = models.CASCADE)
    reg_no         = models.CharField(_("Numero de Registration"),max_length=30,null=True,blank=True,unique=True)
    gender         = models.CharField(_("Options"), max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    first_name     = models.CharField(_("First Name"), max_length=255, null=False, blank=False)
    last_name      = models.CharField(_("Last Name"), max_length=255, null=False, blank=False)
    date_of_birth  = models.DateField(_("Date de Naissance"), blank=True, null=True)
    phone          = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    email          = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    photo          = models.ImageField(_("Photo"), upload_to='Images/%Y/%m/', null=True, blank=True)
    age            = models.IntegerField(_("Age"),default='0', blank=True, null=True)
    address        = models.CharField(_("Address Patient"), max_length=255,null=True,blank=True)
    date_admitted  = models.DateTimeField(_("Date Admission"), auto_now_add=True, auto_now=False)
    last_updated   = models.DateTimeField(_("Derniere Mise a jour"), auto_now_add=False, auto_now=True)
    active         = models.BooleanField(_("Est actif"), default=True)
    timestamp      = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated        = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug           = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    def __str__(self):
        return str(self.admin)
    class Meta:
        ordering = ('-timestamp',)











# PHARMACIST MODEL
class Pharmacist(models.Model):
    STATUS_CHOICES=(
        ('Masculin','Masculin'),
        ('Feminin','Feminin'),
    )
    # admin       = models.OneToOneField(User,null=True, on_delete = models.CASCADE)
    emp_no      =models.CharField(_("Numero de Service(Travail)"),max_length=30,null=True,blank=True,unique=True)
    age         = models.IntegerField(_("Age"),default='0', blank=True, null=True)
    gender      = models.CharField(_("Options"), max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    phone       = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    address     = models.CharField(_("Address Patient"), max_length=255,null=True,blank=True)
    photo       = models.ImageField(_("Photo"), upload_to='Images/%Y/%m/', null=True, blank=True)
    created_at  = models.DateTimeField(_("Date de Creation"),auto_now_add=True)
    active      = models.BooleanField(_("Est actif"), default=True)
    timestamp   = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug        = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    # objects = models.Manager()
    def __str__(self):
        return str(self.admin)

    class Meta:
        ordering = ('-timestamp',)





# SUPPLIER MODEL

class Supplier(models.Model):
    name            = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    email           = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    phone           = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    country        = CountryField(_("Pays"), max_length=255, null=True, blank=True)
    city            = models.CharField(_("Ville"), max_length=255, null=True, blank=True)
    address         = models.CharField(_("Adresse"), max_length=255, null=True, blank=True)
    website         = models.URLField(_("Site Web"), max_length=255, null=True, blank=True)
    facebook_link   = models.URLField(_("Lien Facebook"), max_length=255, null=True, blank=True)
    twitter_link    = models.URLField(_("Lien Twitter"), max_length=255, null=True, blank=True)
    instagram_link  = models.URLField(_("Lien  Instagram"), max_length=255, null=True, blank=True)
    active          = models.BooleanField(_("Est actif"), default=True)
    timestamp       = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated         = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    # created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="provider_created_by")
    
    def __str__(self):
        return self.name






# STOCK MODEL
class Stock(models.Model):
    supplier    = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, related_name="supplier")
    quantity    = models.PositiveIntegerField(_("Quantité"), null=True, blank=True, default=1)
    total       = models.DecimalField(_("Total(cfa)"), decimal_places=2, max_digits=7, null=False, blank=False)
    description = models.TextField(_("Description"), null=False, blank=False)
    active      = models.BooleanField(_("Est actif"), default=True)
    timestamp   = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.supplier.name

    class Meta:
        ordering = ('-timestamp',)









# PRODUCT IMAGE MODEL
class ProductImage(models.Model):
    file       = models.FileField(_("Fichier(pdf,image)"), upload_to="Product/%Y/%m/%d/", null=False, blank=False)
    name       = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)







# PRODUCT CATEGORY MODEL

class ProductCategory(models.Model):
    name       = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug       = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)










# PRODUCT MODEL

class Product(models.Model):
    category      = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_Image")
    stock         = models.ForeignKey(Stock, on_delete=models.SET_NULL, blank=True, null=True, related_name="stock")
    name          = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    unity_price   = models.DecimalField(_("Prix Unitaire"), decimal_places=2, max_digits=7, null=True, blank=True)
    quantity      = models.PositiveIntegerField(_("Quantité"), null=True, blank=True, default=1)
    discount      = models.DecimalField(_("Reduction"), decimal_places=2, max_digits=15, null=False, blank=False)
    product_image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_category")
    photo         = models.ImageField(_("Photo"), upload_to='Images/%Y/%m/', null=True, blank=True)
    brand_name    = models.CharField(_("Nom Commercial"), max_length=255, null=False, blank=False, unique=True)
    genetic_name  = models.CharField(_("Nom Générique"), max_length=255, null=False, blank=False, unique=True)
    description   = models.TextField(_("Description"), null=False, blank=False)
    # producer            = models.CharField(_("Nom du Fabrican"), max_length=255, null=False, blank=False, unique=True)
    active        = models.BooleanField(_("Est actif"), default=True)
    timestamp     = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug          = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)
        









