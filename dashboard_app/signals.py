# signals.py

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *








# CREATE USER PROFILE
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()










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



