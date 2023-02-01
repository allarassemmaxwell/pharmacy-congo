from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import *


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
