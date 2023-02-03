from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import *




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
            'message':   forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'cols':30}),
        }





#  BLOG FORM

class BlogCommentForm(forms.ModelForm):
    class  Meta:
        model = BlogComment
        fields = [
            "blog",
            "name",
            "email",
            "website",
            "comment",
        ]
        widgets = {
            'blog':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'website':forms.URLInput(attrs={'class': 'form-control'}),
            'comment':forms.Textarea(attrs={'class': 'form-control', 'rows':5}),   
        }