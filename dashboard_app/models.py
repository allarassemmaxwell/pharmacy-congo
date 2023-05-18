# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.conf import settings

import uuid
from django.db import models
from django.db.models.fields import DateField

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.core import validators

from landing_app.models import *
from django.urls import reverse

import random   
import string  
import secrets 

from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django.contrib import messages
from decimal import Decimal






# GENERATE RANDOM STRING WITH LENGTH 
def random_string(num):   
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
    return str(res)







# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True
    def save_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("L'email donné doit être défini"))
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('is_superuser doit être vrai'))
        extra_fields['is_staff'] = True
        return self.save_user(email, password, **extra_fields) 
    





ROLE = (
    ("Patient", _("Patient")),
    ("Docteur", _("Docteur")),
    ("Admin", _("Admin")),
)

class User(AbstractBaseUser, PermissionsMixin):
    id         = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("Nom"), max_length=255,)
    last_name  = models.CharField(_("Prénom"), max_length=255,)
    email      = models.EmailField(_("Email"), max_length=200, unique=True, validators = [validators.EmailValidator()])
    is_staff   = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)
    i_agree    = models.BooleanField(_("Terms and conditions"), blank=True, null=True, default=False)
    role       = models.CharField(_("Rôle"), max_length=100, choices=ROLE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def delete_url(self):
        return reverse("user_delete", args=[str(self.id)])

        # GET ALERT DETAIL ABSOLUTE URL
    def update_url(self):
        return reverse("user_update", args=[str(self.id)])













# PROFILE MODEL

class Profile(models.Model):
    STATUS_CHOICES = (
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
    )
    user 	      = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="user_profile")
    photo         = models.ImageField(_("Photo"), upload_to='Images/%Y/%m/', null=True, blank=True)
    phone         = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(_("Date de Naissance"), blank=True, null=True)
    country       = CountryField(_("Pays"), max_length=255, null=True, blank=True)
    city          = models.CharField(_("Ville"), max_length=255, null=True, blank=True)
    address       = models.CharField(_("Adresse"), max_length=255, null=True, blank=True)
    gender        = models.CharField(_("Sexe"), max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    position      = models.CharField(_("Profession"), max_length=255, null=True, blank=True)
    facebook      = models.URLField(_("Lien de Facebook"), max_length=255, null=True, blank=True)
    instagram     = models.URLField(_("Lien de Instagram"), max_length=255, null=True, blank=True)
    twitter       = models.URLField(_("Lien de Twitter"), max_length=255, null=True, blank=True)
    linked_in     = models.URLField(_("Lien de LinkedIn"), max_length=255, null=True, blank=True)
    active        = models.BooleanField(_("Est actif"), default=True)
    timestamp     = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        ordering = ('-timestamp',)









# SUPPLIER MODEL

class Supplier(models.Model):
    name            = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    email           = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    phone           = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    country         = CountryField(_("Pays"), max_length=255, null=True, blank=True)
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
    slug            = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.name

    def delete_url(self):
        return reverse("supplier_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("supplier_update", args=[str(self.slug)])






class StockCategory(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug       = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    def __str__(self):
        return self.name
    
    
    def delete_url(self):
        return reverse("stock_category_delete", args=[str(self.slug)])
    

    def update_url(self):
        return reverse("stock_category_update", args=[str(self.slug)])

    class Meta:
        ordering = ('-timestamp',)









# STOCK MODEL
class Stock(models.Model):
    id               = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    supplier         = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, related_name="supplier")
    category         = models.ForeignKey(StockCategory, on_delete=models.CASCADE, blank=True)
    item_name        = models.CharField(_("Nom Produit"),max_length=50, blank=True, null=True)
    receive_quantity = models.IntegerField(_("Quantité Reçue"), default='0', blank=True, null=True)
    receive_by       = models.CharField(_("Reçue Par"), max_length=50, blank=True, null=True)
    issue_quantity   = models.IntegerField(_("Quantité d'émission"), default='0', blank=True, null=True)
    issue_by         = models.CharField(_("Emis par"), max_length=50, blank=True, null=True)
    issue_to         = models.CharField(_("Emis a"), max_length=50, blank=True, null=True)
    phone_number     = models.CharField(_("Numero de Telephone"), max_length=50, blank=True, null=True)
    created_by       = models.CharField(_("Créé par"), max_length=50, blank=True, null=True)
    reorder_level    = models.IntegerField(_("Niveau de réapprovisionnement"), default='0', blank=True, null=True)
    # product_stock =  models.CharField(_("Nom Produit"), max_length=255, null=False, blank=False, unique=True)
    quantity         = models.PositiveIntegerField(_("Quantité"), null=True, blank=True, default=1)
    unity_price      = models.DecimalField(_("Prix Unitaire"), decimal_places=2, max_digits=7, null=True, blank=True)
    total            = models.DecimalField(_("Total(cfa)"), decimal_places=2, max_digits=7, null=False, blank=False)
    description      = models.TextField(_("Description"), null=False, blank=False)
    export_to_CSV    = models.BooleanField(_("Export en CSV"), default=False)
    active           = models.BooleanField(_("Est actif"), default=True)
    timestamp        = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated          = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return str(self.timestamp)

    def delete_url(self):
        return reverse("stock_delete", args=[str(self.id)])

    def update_url(self):
        return reverse("stock_update", args=[str(self.id)])
    


    class Meta:
        ordering = ('-timestamp',)










# PRODUCT IMAGE MODEL
class ProductImage(models.Model):
    file       = models.FileField(_("Fichier(png, jpeg, jpg)"), upload_to="Product/%Y/%m/%d/", null=False, blank=False)
    name       = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug       = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.name

    def delete_url(self):
        return reverse("product_image_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("product_image_update", args=[str(self.slug)])

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

    def delete_url(self):
        return reverse("product_category_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("product_category_update", args=[str(self.slug)])

    class Meta:
        ordering = ('-timestamp',)












# PRODUCT MODEL

class Product(models.Model):
    category      = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_category")
    stock         = models.ForeignKey(Stock, on_delete=models.SET_NULL, blank=True, null=True, related_name="stock")
    name          = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    unity_price   = models.DecimalField(_("Prix Unitaire"), decimal_places=2, max_digits=7, null=True, blank=True)
    quantity      = models.PositiveIntegerField(_("Quantité"), null=True, blank=True, default=1)
    discount      = models.DecimalField(_("Reduction"), decimal_places=2, max_digits=15, null=True, blank=True)
    image         = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_image")
    brand_name    = models.CharField(_("Nom Commercial"), max_length=255, null=False, blank=False, unique=True)
    genetic_name  = models.CharField(_("Nom Générique"), max_length=255, null=False, blank=False, unique=True)
    # producer      = models.CharField(_("Nom du Fabrican"), max_length=255, null=False, blank=False, unique=True)
    description   = models.TextField(_("Description"), null=False, blank=False)
    active        = models.BooleanField(_("Est actif"), default=True)
    timestamp     = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug          = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.name
    
    def landing_get_detail_url(self):
        return reverse("landing:product_detail", args=[str(self.slug)])

    def delete_url(self):
        return reverse("product_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("product_update", args=[str(self.slug)])

    class Meta:
        ordering = ('-timestamp',)
        













# PATIENT MODEL
class Patient(models.Model):
    SEXE_CHOICES=(
        ('Masculin','Masculin'),
        ('Feminin','Feminin'),
    )
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null=True, blank=True)
    first_name    = models.CharField(_("Nom"), max_length=255, null=True, blank=True)
    last_name     = models.CharField(_("Prénom"), max_length=255, null=True, blank=True)
    reg_no        = models.CharField(_("Numero de Registration"),max_length=30, null=True, blank=True, unique=True)
    profession    = models.CharField(_("Profession"), max_length=255, null=True, blank=True)
    gender        = models.CharField(_("Sexe"), max_length=100, choices=SEXE_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(_("Date de Naissance"), blank=True, null=True)
    phone         = models.CharField(_("Numéro de téléphone"), max_length=25, null=True, blank=True)
    country       = CountryField(_("Pays"), max_length=255, null=True, blank=True)
    city          = models.CharField(_("Ville"), max_length=255, null=True, blank=True)
    address       = models.CharField(_("Address"), max_length=255, null=True, blank=True)
    active        = models.BooleanField(_("Est actif"), default=True)
    timestamp     = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug          = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        if self.user:
            return str(self.user.first_name)+" "+str(self.user.last_name)
        else:
            return str(self.first_name)+" "+str(self.last_name)

    def get_name(self):
        if self.user:
            return str(self.user.first_name)+" "+str(self.user.last_name)
        else:
            return str(self.first_name)+" "+str(self.last_name)
        
    def get_gender(self):
        if self.gender:
            return self.gender
        else:
            if self.user.user_profile.gender:
                return self.user.user_profile.gender
            else:
                return "Sexe est vide"

    def get_phone(self):
        if self.user:
            if self.user.user_profile.phone:
                return self.user.user_profile.phone
            else:
                return "Le téléphone est manquant"
        else:
            if self.phone:
                return self.phone
            else:
                return "Le téléphone est manquant"

    def get_date_of_birth(self):
        if self.user:
            if self.user.user_profile.date_of_birth:
                return self.user.user_profile.date_of_birth
            else:
                return "La date de naissance est manquante"
        else:
            if self.date_of_birth:
                return self.date_of_birth
            else:
                return "La date de naissance est manquante"
    
    def delete_patient_url(self):
        if self.user:
            return reverse("patient_user_delete", args=[str(self.slug)])
        else:
            return reverse("patient_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("patient_update", args=[str(self.slug)])
    class Meta:
        ordering = ('-timestamp',)







# SALE MODEL
class Sale(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=False, null=True, related_name="sale_product")
    quantity    = models.PositiveIntegerField(_("Quantité"), null=True, blank=False, default=1)
    unity_price = models.DecimalField(_("Prix Unitaire"), decimal_places=2, max_digits=7, null=True, blank=False)
    total       = models.DecimalField(_("Total"), decimal_places=2, max_digits=15, null=True, blank=True)
    recu        = models.FileField(_("Fichier(pdf,image)"), upload_to="Recu/%Y/%m/%d/", null=False, blank=False)
    active      = models.BooleanField(_("Est actif"), default=True)
    timestamp   = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.reference
    
    def delete_url(self):
        return reverse("sale_delete", args=[str(self.id)])
    def update_url(self):
        return reverse("sale_update", args=[str(self.id)])

    class Meta:
        ordering = ('-timestamp',)









# APPOINTMENT SYMPTOM MODEL
class AppointmentSymptom(models.Model):
    name       = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug       = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.name

    def delete_url(self):
        return reverse("appointment_symptom_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("appointment_symptom_update", args=[str(self.slug)])

    class Meta:
        ordering = ('-timestamp',)
















# APPOINTMENT MODEL
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
    )
    HOUR_CHOICES = (
        ('8h:00mn', '8h:00mn'),
        ('8h:30mn', '8h:30mn'),
        ('9h:00mn', '9h:00mn'),
        ('9h:30mn', '9h:30mn'),
        ('10h:00mn', '10h:00mn'),
        ('10h:30mn', '10h:30mn'),
        ('11h:00mn', '11h:00mn'),
        ('11h:30mn', '11h:30mn'),
        ('12h:00mn', '12h:00mn'),
        ('12h:30mn', '12h:30mn'),
        ('13h:00mn', '13h:00mn'),
        ('13h:30mn', '13h:30mn'),
        ('14h:00mn', '14h:00mn'),
        ('14h:30mn', '14h:30mn'),
        ('15h:00mn', '15h:00mn'),
        ('15h:30mn', '15h:30mn'),
        ('16h:00mn', '16h:00mn'),
        ('16h:30mn', '16h:30mn'),
        ('17h:00mn', '17h:00mn'),
    )
    id          = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    patient     = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=False, null=True)
    subject     = models.CharField(_("Sujet"), max_length=255, null=False, blank=False)
    date        = models.DateField(_("Date"), blank=False, null=False)
    hour        = models.CharField(_("Horaire"), max_length=25, choices=HOUR_CHOICES, null=False, blank=False)
    description = models.TextField(_("Description"), null=False, blank=False)
    read        = models.BooleanField(_("Lu"), default=False)
    active      = models.BooleanField(_("Est actif"), default=True)
    timestamp   = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return "%s le %s à %s"%(self.patient, self.date, self.hour)

    class Meta:
        ordering = ('-timestamp',)

    def delete_url(self):
        return reverse("appointment_delete", args=[str(self.id)])
    
    def update_url(self):
        return reverse("appointment_update", args=[str(self.id)])











# APPOINTMENT PRESCRIPTION MODEL
class AppointmentPrescription(models.Model):
    appointment      = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=False, null=True, related_name="prescription_appointment")
    weight           = models.DecimalField(_("Poids"), decimal_places=2, max_digits=5, null=False, blank=False)
    body_temperature = models.DecimalField(_("Température Corporelle"), decimal_places=2, max_digits=5, null=False, blank=False)
    symptoms         = models.ManyToManyField(AppointmentSymptom, blank=True)
    price            = models.DecimalField(_("Prix payé"), decimal_places=2, max_digits=15, null=False, blank=False)
    received_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="prescription_received_by")
    description      = models.TextField(_("Description"), null=True, blank=False)
    active           = models.BooleanField(_("Est actif"), default=True)
    timestamp        = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated          = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return str(self.id)
    
    
    def delete_url(self):
        return reverse("appointment_prescription_delete", args=[str(self.id)])
    def update_url(self):
        return reverse("appointment_prescription_update", args=[str(self.id)])

    class Meta:
        ordering = ('-timestamp',)













# BLOG CATEGORY MODEL
class ServiceCategory(models.Model):
    name        = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active      = models.BooleanField(_("Active"), default=True)
    timestamp   = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug        = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.name

    def delete_url(self):
        return reverse("service_category_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("service_category_update", args=[str(self.slug)])

    class Meta:
        ordering = ("-timestamp",)
    
    # verbose_name_plural = _('BlogCategories')








# SERVICE MODEL
class Service(models.Model):
    category    = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=False, blank=False, related_name="service_category")
    name        = models.CharField(_("Nom"), max_length=255, null=False, blank=False)
    photo       = models.ImageField(_("Image"), upload_to="Service/%Y/%m/%d/", null=True, blank=True)
    description = models.TextField(_("Description"), null=False, blank=False)
    active      = models.BooleanField(_("Active"), default=True)
    timestamp   = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)
    slug        = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)

    def __str__(self):
        return self.name

    # GET ALERT DETAIL ABSOLUTE URL
    def get_detail_url(self):
        return reverse("landing:service_detail", args=[str(self.slug)])

    def delete_url(self):
        return reverse("service_delete", args=[str(self.slug)])

    def update_url(self):
        return reverse("service_update", args=[str(self.slug)])

    class Meta:
        ordering = ("-timestamp",)











# NOTIFICATION MODELS
class Notification(models.Model):
    contact     = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, related_name="notification_contact")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name="notification_appointment")
    subject     = models.CharField(_("Sujet"), max_length=255, null=True, blank=False)
    read        = models.BooleanField(_("Lu"), default=False)
    active      = models.BooleanField(_("Est actif"), default=True)
    timestamp   = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug        = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.contact
        
    
    def read_url(self):
        if self.contact:
            return reverse("contact_respond", args=[str(self.contact.slug)])
        elif self.appointment:
            return reverse("appointment_detail", args=[str(self.appointment.id)])
    
    class Meta:
        ordering = ("-timestamp",)












# FRIDGE MODEL

class Fridge(models.Model):
    STATE_CHOICES=(
        ('Normal','Normal'),
        ('Probleme_Mineur','Probleme_Mineur'),
        ('Probleme_Critique','Probleme_Critique'),
    )
    
    ENERGY_CHOICES=(
        ('Solaire','Solaire'),
        ('Electrique','Electrique'),
    )
    name             = models.CharField(_("Nom du Frigo"), max_length=255, null=False, blank=False, unique=True)
    marque           = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    code_pqs         = models.CharField(_("Code PQS"), max_length=255, null=False, blank=False, unique=True)
    date_acquisition = models.DateField(_("Date Acquisition"), blank=True, null=True)
    photo            = models.ImageField(_("Image"), upload_to="Service/%Y/%m/%d/", null=True, blank=True)
    price            = models.DecimalField(_("Prix Frigidaire"), decimal_places=2, max_digits=7, null=True, blank=True)
    state            = models.CharField(_("Etat du Frigidaire"), max_length=100, choices=STATE_CHOICES, null=True, blank=True)
    fix_number       = models.PositiveIntegerField(_("Nombre de Reparation"), null=True, blank=False, default=1)
    energy           = models.CharField(_("Energie Utilisée"), max_length=100, choices=ENERGY_CHOICES, null=True, blank=True)
    active           = models.BooleanField(_("Est actif"), default=True)
    timestamp        = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated          = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    # slug             = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.name

    def delete_url(self):
        return reverse("fridge_delete", args=[str(self.id)])

    def update_url(self):
        return reverse("fridge_update", args=[str(self.id)])

    class Meta:
        ordering = ('-timestamp',)
        





















# INVOICE MODEL

class Invoice(models.Model):
    PAYMENT_CHOICES=(
        ('Carte Bancaire', 'Carte Bancaire'),
        ('Cheques', 'Cheques'),
        ('Cash', 'Cash'),
        ('En Attente', 'En Attente'),
    )
    
    INVOICE_CHOICES=(
        ('Proformat', 'Proformat'),
        ('Facture', 'Facture'),
        ('Reçu', 'Reçu'),
        
    )
    # order_id           = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    customer_name      = models.CharField(_("Nom du Client"), max_length=255, null=False, blank=False, unique=True)
    customer_phone     = models.CharField(_("Téléphone Client"), max_length=255, null=False, blank=False, unique=True)
    customer_address   = models.CharField(_("Addresse Client"), max_length=255, null=False, blank=False, unique=True)
    doc_name           = models.CharField(_("Nom du Personel"), max_length=255, null=False, blank=False, unique=True)
    doc_phone          = models.CharField(_("Téléphone Personel"), max_length=255, null=False, blank=False, unique=True)
    doc_address        = models.CharField(_("Addresse Personel"), max_length=255, null=False, blank=False, unique=True)
    payment_mode       = models.CharField(_("Mode de Paiement"), max_length=100, choices=PAYMENT_CHOICES, null=True, blank=True)
    unity_price        = models.DecimalField(_("Prix Unitaire"), decimal_places=2, max_digits=7, null=True, blank=True)
    quantity           = models.PositiveIntegerField(_("Quantité"), null=True, blank=True, default=1)
    vat                = models.DecimalField(_("TVA du Produit"), decimal_places=2, max_digits=7, null=True, blank=True)
    description        = models.CharField(_("Designation du Produit"), max_length=255, null=False, blank=False, unique=True)
    issued_date        = models.DateField(_("Date D'emission"), blank=True, null=True, auto_now_add=True)
    payment_date       = models.DateField(_("Date de paiement"), blank=True, null=True)
    invoice_type       = models.CharField(_("Type de Facturation"), max_length=100, choices=INVOICE_CHOICES, null=True, blank=True)
    
    total              = models.DecimalField(_("Total Produit par Ligne (cfa)"), decimal_places=2, max_digits=7, null=False, blank=False)
    sub_total          = models.DecimalField(_("Sous Total (cfa)"), decimal_places=2, max_digits=7, null=True, blank=False)
    global_total       = models.DecimalField(_("Total Global (cfa)"), decimal_places=2, max_digits=7, null=True, blank=False)
    
    active             = models.BooleanField(_("Est actif"), default=True)
    timestamp          = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated            = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    # slug             = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.customer_name

    def delete_url(self):
        return reverse("invoice_delete", args=[str(self.id)])

    def update_url(self):
        return reverse("invoice_update", args=[str(self.id)])


    class Meta:
        ordering = ('-timestamp',)
        
