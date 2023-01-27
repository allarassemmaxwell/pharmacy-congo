# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.conf import settings

import uuid
from django.db import models
from django.db.models.fields import DateField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import  gettext_lazy as _


from django.core import validators

from django.urls import reverse

import random   
import string  
import secrets 

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from decimal import Decimal


# Create your Models here.
# ==========================================================================
#                            LANDING PAGE MODELS
# ==========================================================================





# CONTACT MODEL
class Contact(models.Model):
    first_name     = models.CharField(_("First Name"), max_length=255, null=False, blank=False)
    last_name      = models.CharField(_("Last Name"), max_length=255, null=False, blank=False)
    email          = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    subject        = models.CharField(_("Subject"), max_length=255, null=False, blank=False)
    phone          = models.CharField(_("Phone"), max_length=255, null=False, blank=False)
    message        = models.TextField(_("Message"), null=False, blank=False)
    active         = models.BooleanField(_("Active"), default=True)
    timestamp      = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated        = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)

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







# BLOG MODEL
class Blog(models.Model):
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
    
    class Meta:
        ordering = ("-timestamp",)
        






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
    full_name        = models.CharField(_("Full Name"), max_length=255, null=False, blank=False)
    image       = models.ImageField(_("Image"), upload_to='Testimony/%Y/%m/', null=True, blank=True)
    occupation  = models.CharField(_("Occupation"), max_length=255, null=False, blank=False)
    description = models.TextField(_("Description"), null=False, blank=False)
    active      = models.BooleanField(_("Status"), default=True)
    timestamp   = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.full_name


    class Meta:
        ordering = ('-timestamp',)
        verbose_name_plural = _('Testimonies')








# ==========================================================================
#                            DASHBOARD PAGE MODELS
# ==========================================================================




# PROFILE MODEL

class Profile(models.Model):
    STATUS_CHOICES = (
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
    )
    user          = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="employee_user")
    photo         = models.ImageField(_("Photo"), upload_to='Images/%Y/%m/', null=True, blank=True)
    phone         = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(_("Date de Naissance"), blank=False, null=False)
    country       = models.CharField(_("Pays"), max_length=255, null=True, blank=True)
    city          = models.CharField(_("Ville"), max_length=255, null=True, blank=True)
    address       = models.CharField(_("Adresse"), max_length=255, null=True, blank=True)
    gender        = models.CharField(_("Options"), max_length=100, choices=STATUS_CHOICES, null=False, blank=False)
    position      = models.CharField(_("Pays"), max_length=255, null=True, blank=True)
    active        = models.BooleanField(_("Est actif"), default=True)
    timestamp     = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return str(self.user.get_full_name)

    class Meta:
        ordering = ('-timestamp',)









# SUPPLIER MODEL

class Supplier(models.Model):
    name            = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    email           = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    phone           = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    country         = models.CharField(_("Pays"), max_length=255, null=True, blank=True)
    city            = models.CharField(_("Ville"), max_length=255, null=True, blank=True)
    address         = models.CharField(_("Adresse"), max_length=255, null=True, blank=True)
    website         = models.URLField(_("Site Web"), max_length=255, null=True, blank=True)
    facebook_link   = models.URLField(_("Lien Facebook"), max_length=255, null=True, blank=True)
    twitter_link    = models.URLField(_("Lien Twitter"), max_length=255, null=True, blank=True)
    instagram_link  = models.URLField(_("Lien  Instagram"), max_length=255, null=True, blank=True)
    active          = models.BooleanField(_("Est actif"), default=True)
    timestamp       = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated         = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="provider_created_by")
    
    def __str__(self):
        return self.name









# STOCK MODEL

class Stock(models.Model):
    supplier     = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, related_name="supplier")
    quantity     = models.CharField(_("Quantité"), max_length=255, null=True, blank=True)
    total        = models.CharField(_("Total"), max_length=255, null=True, blank=True)
    description  = models.TextField(_("Description"), null=False, blank=False)
    active       = models.BooleanField(_("Est actif"), default=True)
    timestamp    = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated      = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.business.name

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
    unity_price   = models.CharField(_("Prix Unitaire"), max_length=255, null=True, blank=True)
    quantity      = models.CharField(_("Quantité"), max_length=255, null=True, blank=True)
    discount      = models.DecimalField(_("Reduction"), decimal_places=2, max_digits=15, null=False, blank=False)
    product_image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_category")
    brand_name    = models.CharField(_("Nom Commercial"), max_length=255, null=False, blank=False, unique=True)
    genetic_name  = models.CharField(_("Nom Générique"), max_length=255, null=False, blank=False, unique=True)
    description   = models.TextField(_("Description"), null=False, blank=False)
    active        = models.BooleanField(_("Est actif"), default=True)
    timestamp     = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug          = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)
        










# SALE MODEL

class Sale(models.Model):
    reference  = models.CharField(_("Reference"), max_length=255, null=False, blank=False, unique=True)
    product    = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name="product")
    quantity   = models.DecimalField(_("Quantité"), decimal_places=2, max_digits=15, null=False, blank=False)
    total      = models.DecimalField(_("Total"), decimal_places=2, max_digits=15, null=False, blank=False)
    recu       = models.FileField(_("Fichier(pdf,image)"), upload_to="Recu/%Y/%m/%d/", null=False, blank=False)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)









# APPOINTMENT SYMPTOM MODEL

class AppointmentSymptom(models.Model):
    name       = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)









# APPOINTMENT MODEL

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
    )
    first_name   = models.CharField(_("First Name"), max_length=255, null=False, blank=False)
    last_name    = models.CharField(_("Last Name"), max_length=255, null=False, blank=False)
    email        = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    phone        = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    subject      = models.CharField(_("Sujet"), max_length=255, null=False, blank=False, unique=True)
    gender       = models.CharField(_("Options"), max_length=100, choices=STATUS_CHOICES, null=False, blank=False)
    # 👉 try to see the field age 🔥
    age          = models.IntegerField(_("Age"),  null=False, blank=False)
    hour         = models.DateTimeField(_("Horaire Rv"), auto_now_add=True, auto_now=False)
    date         = models.DateField(_("Date de RV"), blank=False, null=False)
    description  = models.TextField(_("Description"), null=False, blank=False)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)










# APPOINTMENT PRESCRIPTION MODEL

class AppointmentPrescription(models.Model):
    product_name       = models.CharField(_("Nom du Produit"), max_length=255, null=False, blank=False, unique=True)
    quantity   = models.DecimalField(_("Quantité"), decimal_places=2, max_digits=15, null=False, blank=False)
    heart_rate   = models.DecimalField(_("Pression Cardiac"), decimal_places=2, max_digits=15, null=False, blank=False)
    weight   = models.DecimalField(_("Poids"), decimal_places=2, max_digits=15, null=False, blank=False)
    blood_rate   = models.DecimalField(_("Taux Sanguin"), decimal_places=2, max_digits=15, null=False, blank=False)
    body_temperature   = models.DecimalField(_("Temperature Corporelle"), decimal_places=2, max_digits=15, null=False, blank=False)
    glucose_level       = models.DecimalField(_("Taux de Glucose"), decimal_places=2, max_digits=15, null=False, blank=False)
    blood_pressure      = models.DecimalField(_("Pression Sanguine"), decimal_places=2, max_digits=15, null=False, blank=False)
    day                 = models.DateField(_("Jour de RV"), blank=False, null=False)
    appointment_symptom = models.TextField(_("Symptome Patient"), null=False, blank=False)
    morning_times       = models.BooleanField(_("Matin"), default=False)
    afternoon_times     = models.BooleanField(_("Apres Midi"), default=False)
    evening_times       = models.BooleanField(_("Soir"), default=True)
    night_times         = models.BooleanField(_("Nuit"), default=True)
    appointment         = models.ForeignKey(Appointment, on_delete=models.SET_NULL, blank=True, null=True, related_name="product")
    price               = models.DecimalField(_("Prix"), decimal_places=2, max_digits=15, null=False, blank=False)
    by                  = models.CharField(_("Nom du Pharmacien(e)"), max_length=255, null=False, blank=False, unique=True)
    active              = models.BooleanField(_("Est actif"), default=True)
    timestamp           = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)