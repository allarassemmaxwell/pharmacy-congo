from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import *
from allauth.account.forms import SignupForm

from django.core.files.images import get_image_dimensions
User = get_user_model()

from django.forms.widgets import CheckboxInput
from datetime import date



from .models import *
from landing_app.models import *






class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Nom', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name  = forms.CharField(max_length=50, label='Prénom', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email     = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    i_agree   = forms.BooleanField(label=mark_safe(_("En vous inscrivant, vous acceptez le ... (<a href='/terms-and-conditions/' target='_blank'>Conditions d'utilisation</a>)")), required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'i_agree', 'email', 'password1', 'password2']

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.role = 'Patient'
        profile = Profile.objects.create(user = user)
        patient = Patient.objects.create(user = user, reg_no = random_string(7))
        user.save()
        profile.save()
        patient.save()
        return user








# BRANCH FORM
class UserForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "role"
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'role':       forms.Select(attrs={'class': 'form-control'}),
        }








# BRANCH FORM
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = [
            "first_name",
            "last_name",
            "role"
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'role':       forms.Select(attrs={'class': 'form-control'}),
        }










# PROFILE FORM
class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = [
            "photo",
            "phone",
            "date_of_birth",
            "country",
            "city",
            "address",
            "gender",
            "position",
            "facebook",
            "instagram",
            "twitter",
            "linked_in",
        ]
        widgets = {
            'phone':    forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country':   forms.Select(attrs={'class': 'form-control'}),
            'city':      forms.TextInput(attrs={'class': 'form-control'}),
            'address':   forms.TextInput(attrs={'class': 'form-control'}),
            'gender':    forms.Select(attrs={'class': 'form-control'}),
            'position':  forms.TextInput(attrs={'class': 'form-control'}),
            'facebook':  forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter':   forms.URLInput(attrs={'class': 'form-control'}),
            'linked_in': forms.URLInput(attrs={'class': 'form-control'}),
        }










# BRANCH FORM
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model  = ProductCategory
        fields = [
            "name",
        ]
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
        }







# BRANCH FORM
class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model  = ServiceCategory
        fields = [
            "name",
        ]
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
        }








# BRANCH FORM
class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = [
            "category",
            "stock",
            "name",
            "unity_price",
            "quantity",
            "discount",
            "product_image",
            "brand_name",
            "genetic_name",
            "description"
        ]
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
            # 'category':    forms.Select(attrs={'class': 'form-control select2', 'data-toggle':'select2'}),
            # 'photo':    forms.FileInput(attrs={'class': 'form-control'}),
            'unity_price':    forms.NumberInput(attrs={'step': 0.25, 'class': 'form-control'}),
            'quantity':    forms.NumberInput(attrs={'step': 0.25, 'class': 'form-control'}),
            'discount':    forms.NumberInput(attrs={'step': 0.25, 'class': 'form-control'}),
            # 'since': forms.DateInput(attrs={'class': 'form-control', 'data-date-format':'yyyy-mm-dd', 'data-provide':'datepicker', 'data-date-autoclose':'true'}, format='%Y-%m-%d'),
            'brand_name':     forms.TextInput(attrs={'class': 'form-control'}),
            'genetic_name':     forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
        }
    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     since = cleaned_data.get('since')
    #     if since > date.today():
    #         self.add_error('since', "Année doit être inférieure à la date d'aujourd'hui.")
    #     return cleaned_data








# BRANCH FORM
class ProductImageForm(forms.ModelForm):
    class Meta:
        model  = ProductImage
        fields = [
            "name",
            "file",
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class':'form-control-file', 'accept':'.png, .jpeg, .jpg'}),
        }





# BLOG CATEGORY FORM
class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model  = BlogCategory
        fields = [
            "name",
        ]
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
        }









# BLOG FORM
class BlogForm(forms.ModelForm):
    class Meta:
        model  = Blog
        fields = [
            "category",
            "name",
            "photo",
            "description",
        ]
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
        }






 
# PARTNER FORM
class PartnerForm(forms.ModelForm):
    class Meta:
        model  = Partner
        fields = [
            "name",
            "logo",
            "website",
        ]
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }






 
# NEWSLETTER FORM
class NewsletterForm(forms.ModelForm):
    class Meta:
        model  = Subscriber
        fields = [
            "email",
            "active"
        ]
        widgets = {
           'email':    forms.TextInput(attrs={'class': 'form-control'}),
        }






# NEWSLETTER FORM
class EmailSubscriberForm(forms.ModelForm):
    class Meta:
        model  = EmailSubscriber
        fields = [
            "name",
            "description",
        ]
        widgets = {
           'name':    forms.TextInput(attrs={'class': 'form-control'}),
           'description': forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
        }






# TESTIMONY FORM
class TestimonyForm(forms.ModelForm):
    class Meta:
        model  = Testimony
        fields = [
            "full_name",
            "image",
            "occupation",
            "description"
        ]
        widgets = {
            'full_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'occupation':    forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
        }








# SERVICE  FORM
class ServiceForm(forms.ModelForm):
    class Meta:
        model  = Service
        fields = [
            "name",
            "category",
            "photo",
            "description"
        ]
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
        }










# CONTACT FORM
class ContactResponseForm(forms.ModelForm):
    class Meta:
        model  = ContactResponse
        fields = [
            "response",
        ]
        widgets = {
            'response': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        }








# SUPPLIER FORM
class SupplierForm(forms.ModelForm):
    class Meta:
        model  = Supplier
        fields = [
            "name",
            "email",
            "phone",
            "country",
            "city",
            "address",
            "website",
            "facebook_link",
            "twitter_link",
            "instagram_link"
        ]
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
            'email':     forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':     forms.TextInput(attrs={'class': 'form-control'}),
            'country':     forms.Select(attrs={'class': 'form-control'}),
            'city':    forms.TextInput(attrs={'class': 'form-control'}),
            'address':    forms.TextInput(attrs={'class': 'form-control'}),
            'website':    forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_link':     forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_link':     forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_link': forms.URLInput(attrs={'class': 'form-control'}),
        }









# STOCK FORM

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            "supplier",
            "quantity",
            # "unity_price",
            "total",
            "description",
            "active",
        ]
        widgets = {
            'quantity':    forms.NumberInput(attrs={'step': 0.25, 'class': 'form-control'}),
            # 'unity_price':    forms.NumberInput(attrs={'step': 0.25, 'class': 'form-control'}),
            'total':    forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.all()
        self.fields['supplier'].label_from_instance = lambda obj: obj.name








# APPOINTMENT SYMPTOMS FORM
class AppointmentSymptomForm(forms.ModelForm):
    class Meta:
        model  = AppointmentSymptom
        fields = [
            "name",
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }










# APPOINTMENT FORM
class AppointmentForm(forms.ModelForm):
    class Meta:
        model  = Appointment
        fields = [
            "patient",
            "subject",
            "date",
            "hour",
            "description"
        ]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'hour': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':7}),
        }











# APPOINTMENT PRESCRIPTION FORM
class AppointmentPrescriptionForm(forms.ModelForm):
    class Meta:
        model  = AppointmentPrescription
        fields = [
            "appointment",
            "weight",
            "body_temperature",
            "symptoms",
            "price",
            "received_by",
            "description"
        ]
        widgets = {
            'appointment':      forms.Select(attrs={'class': 'form-control'}),
            'weight':           forms.NumberInput(attrs={'class': 'form-control'}),
            'body_temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'price':            forms.NumberInput(attrs={'class': 'form-control'}),
            'received_by':      forms.Select(attrs={'class': 'form-control'}),
            'description':      forms.Textarea(attrs={'class': 'form-control', 'rows':7}),
        }













# CONTACT FORM
class ContactForm(forms.ModelForm):
    class Meta:
        model  = Contact
        fields = [
            "first_name",
            "last_name",
            "email",
            "subject",
            "phone",
            "message",
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email':     forms.EmailInput(attrs={'class': 'form-control'}),
            'subject':   forms.TextInput(attrs={'class': 'form-control'}),
            'phone':   forms.TextInput(attrs={'class': 'form-control'}),
            'message':   forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'cols':30}),
        }















# PATIENTS FORM
class PatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required    = True
        self.fields['last_name'].required = True
        self.fields['profession'].required    = True
        self.fields['gender'].required = True
        self.fields['country'].required = True
        self.fields['city'].required = True
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "profession",
            "gender",
            "date_of_birth",
            "phone",
            "country",
            "city",
            "address",        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }












# SALE  FORM
class SaleForm(forms.ModelForm):
    class Meta:
        model  = Sale
        fields = [
            "product",
            "quantity",
            "unity_price",
            "recu"
        ]
        widgets = {
            'product':   forms.Select(attrs={'class': 'form-control'}),
            'quantity':  forms.NumberInput(attrs={'step': 0.25, 'class': 'form-control'}),
            'unity_price':  forms.NumberInput(attrs={'step': 0.25, 'class': 'form-control'}),
        }









# CONTACT FORM
class SubscriberResponseForm(forms.ModelForm):
    class Meta:
        model  = SubscriberResponse
        fields = [
            "subject",
            "message",
        ]
        widgets = {
            'subject':   forms.TextInput(attrs={'class': 'form-control'}),
            'message':   forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'cols':30}),
        }









# NOTIFICATION FORM
class NotificationForm(forms.ModelForm):
    class Meta:
        model  = Notification
        fields = [
            "contact",
            "appointment",
            "subject",
        ]
        widgets = {
           'contact':    forms.Select(attrs={'class': 'form-control'}),
           'appointment':    forms.Select(attrs={'class': 'form-control'}),
           'subject':    forms.TextInput(attrs={'class': 'form-control'}),
        }