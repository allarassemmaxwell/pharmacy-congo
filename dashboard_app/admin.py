# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import *


admin.site.site_header = "Open data"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'role', 'first_name', 'last_name', 'i_agree', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'i_agree', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'is_active', 'role', 'is_staff')
    ordering = ('email',)
    readonly_fields = ('last_login', 'i_agree',)








# # PROFILE ADMIN
class ProfileAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['user', 'phone', 'timestamp', 'updated']
    list_display_links  = ['user',]
    list_filter         = ['user']
    search_fields       = ['user']
    list_per_page       = 50
    class Meta:
        model = Profile
admin.site.register(Profile, ProfileAdmin)





# # PRODUCT CATEGORY ADMIN
class ProductCategoryAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = ProductCategory
admin.site.register(ProductCategory, ProductCategoryAdmin)




#  PRODUCT IMAGE ADMIN
class ProductImageAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = ProductImage
admin.site.register(ProductImage, ProductImageAdmin)











#  PRODUCT ADMIN
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'category', 'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = Product
admin.site.register(Product, ProductAdmin)









#  SERVICE ADMIN
class ServiceCategoryAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = ServiceCategory
admin.site.register(ServiceCategory, ServiceCategoryAdmin)












#  SERVICE ADMIN
class ServiceAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'category', 'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = Service
admin.site.register(Service, ServiceAdmin)








#  STOCK ADMIN
class StockAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['supplier', 'category', 'item_name', 'quantity', 'total', 'description', 'timestamp', 'updated']
    list_display_links  = ['supplier',]
    list_filter         = ['active']
    search_fields       = ['category', 'item_name', 'supplier__name', 'description']
    list_per_page       = 50
    class Meta:
        model = Stock
admin.site.register(Stock, StockAdmin)
admin.site.register(StockCategory)










# SUPPLIER ADMIN
class SupplierAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'country', 'city', 'address',  'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = Supplier
admin.site.register(Supplier, SupplierAdmin)








#  APPOINTMENT SYMPTOM ADMIN
class AppointmentSymptomAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['id', 'timestamp', 'updated']
    list_display_links  = ['id',]
    list_filter         = ['id']
    search_fields       = ['id']
    list_per_page       = 50
    class Meta:
        model = AppointmentSymptom
admin.site.register(AppointmentSymptom, AppointmentSymptomAdmin)









#  APPOINTMENT SYMPTOM ADMIN
class AppointmentAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['subject', 'timestamp', 'updated']
    list_display_links  = ['subject',]
    list_filter         = ['subject']
    search_fields       = ['subject']
    list_per_page       = 50
    class Meta:
        model = Appointment
admin.site.register(Appointment, AppointmentAdmin)










#  PRODUCT ADMIN
class PatientAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['reg_no', 'first_name','last_name', 'timestamp', 'updated']
    list_display_links  = ['first_name',]
    list_filter         = ['first_name']
    search_fields       = ['first_name']
    list_per_page       = 50
    class Meta:
        model = Patient
admin.site.register(Patient, PatientAdmin)











#  SALE ADMIN
class SaleAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['product', 'quantity', 'total', 'timestamp', 'updated']
    list_display_links  = ['product',]
    list_filter         = ['product']
    search_fields       = ['product']
    list_per_page       = 50
    class Meta:
        model = Sale
admin.site.register(Sale, SaleAdmin)










#  NOTIFICATION ADMIN
class NotificationAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['contact', 'appointment', 'subject', 'timestamp', 'updated']
    list_display_links  = ['contact',]
    list_filter         = ['active']
    search_fields       = ['contact', 'appointment']
    list_per_page       = 50
    class Meta:
        model = Notification
admin.site.register(Notification, NotificationAdmin)









#  INVOICE ADMIN
class InvoiceAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['customer_name', 'payment_date', 'payment_mode']
    list_display_links  = ['customer_name',]
    list_filter         = ['active']
    search_fields       = ['customer_name', 'payment_date', 'payment_mode',]
    list_per_page       = 50
    class Meta:
        model = Invoice
admin.site.register(Invoice, InvoiceAdmin)

