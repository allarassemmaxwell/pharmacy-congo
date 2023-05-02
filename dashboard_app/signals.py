# signals.py

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *








# CREATE USER PROFILE
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.user_profile.save()










def create_service_cat_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = ServiceCategory.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_service_cat_slug(instance, new_slug=new_slug)
    return slug

def presave_service_cat(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_service_cat_slug(instance)
pre_save.connect(presave_service_cat, sender=ServiceCategory)








def create_service_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Service.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_service_slug(instance, new_slug=new_slug)
    return slug

def presave_service(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_service_slug(instance)
pre_save.connect(presave_service, sender=Service)









def create_service_supplier_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Supplier.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_service_supplier_slug(instance, new_slug=new_slug)
    return slug

def presave_supplier(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_service_supplier_slug(instance)
pre_save.connect(presave_supplier, sender=Supplier)









def create_product_image_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = ProductImage.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_product_image_slug(instance, new_slug=new_slug)
    return slug

def presave_product_image(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_product_image_slug(instance)
pre_save.connect(presave_product_image, sender=ProductImage)










def create_product_cat_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = ProductCategory.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_product_cat_slug(instance, new_slug=new_slug)
    return slug

def presave_product_cat(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_product_cat_slug(instance)
pre_save.connect(presave_product_cat, sender=ProductCategory)








def create_product_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Product.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_product_slug(instance, new_slug=new_slug)
    return slug

def presave_product(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_product_slug(instance)
pre_save.connect(presave_product, sender=Product)











def create_appoint_symt_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = AppointmentSymptom.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_appoint_symt_slug(instance, new_slug=new_slug)
    return slug

def presave_appoint_symt(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_appoint_symt_slug(instance)
pre_save.connect(presave_appoint_symt, sender=AppointmentSymptom)











def create_patient_slug(instance, new_slug=None):
    slug = slugify(random_string(14))
    if new_slug is not None:
        slug = new_slug
    ourQuery = Patient.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_patient_slug(instance, new_slug=new_slug)
    return slug

def presave_patient(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_patient_slug(instance)
pre_save.connect(presave_patient, sender=Patient)









# CREATE NOTIFICATION SLUG        
def create_notification_slug(instance, new_slug=None):
    slug = random_string(15)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Notification.objects.filter(slug=slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_notification_slug(instance, new_slug=new_slug)
    return slug

def presave_notification(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_notification_slug(instance)
pre_save.connect(presave_notification, sender=Notificaty)



