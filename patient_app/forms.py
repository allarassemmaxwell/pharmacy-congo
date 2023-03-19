from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from dashboard_app.models import *
User = get_user_model()
from datetime import date



from .models import *
from landing_app.models import *









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
            'hour': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':7}),
        }



