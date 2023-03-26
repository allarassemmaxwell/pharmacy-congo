from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from dashboard_app.models import *
User = get_user_model()
from datetime import date
import datetime
from .models import *
from landing_app.models import *













# BRANCH FORM
class PatientUserUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = [
            "first_name",
            "last_name",
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
        }








# PROFILE FORM
class PatientProfileForm(forms.ModelForm):
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







# APPOINTMENT FORM
class PatientAppointmentForm(forms.ModelForm):
    class Meta:
        model  = Appointment
        fields = [
            "subject",
            "date",
            "hour",
            "description"
        ]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
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



