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

import datetime

from .models import *
from dashboard_app.models import *




# CONTACT FORM
class ContactForme(forms.ModelForm):
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
            'message':   forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'cols':30}),
        }




# BLOG COMMENT FORM
class BlogCommentForm(forms.ModelForm):
    class Meta:
        model= BlogComment
        fields= [
            'name',
            'email',
            'comment'
        ]
        
        Widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control form--control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'row':1, 'cols':30}),
        }




#  BLOG FORM

class BlogCommentForm(forms.ModelForm):
    class  Meta:
        model = BlogComment
        fields = [
            "name",
            "email",
            "comment",
        ]
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'comment':forms.Textarea(attrs={'class': 'form-control', 'rows':5}),   
        }





# BRANCH FORM
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
            'subject':     forms.TextInput(attrs={'class': 'form-control'}),
            'date':        forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':7}),
        }
    def clean(self):
        cleaned_data = self.cleaned_data
        date  = cleaned_data.get('date')
        hour  = cleaned_data.get('hour')
        today = datetime.date.today()
        if date < today:
            self.add_error('date', "La date choisie doit être supérieure ou égale à la date d'aujourd'hui")
        check = Appointment.objects.filter(date=date, hour=hour)
        if check:
            self.add_error('hour', "Un autre rendez-vous existe avec la même date et heure")
        return cleaned_data

