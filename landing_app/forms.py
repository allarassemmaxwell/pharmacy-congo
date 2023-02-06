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









# PRODUCT FORM
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "unity_price",
            "quantity",
            "discount",
            "product_image",
            "photo",
            "brand_name",
            "genetic_name",
            "description",
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unity_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_image': forms.URLInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'genetic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 30}),
        }

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount and (discount < 0 or discount > 100):
            raise forms.ValidationError("Discount must be between 0 and 100.")
        return discount










#  PHARMACY FORM

class PharmacyForm(forms.ModelForm):
    class  Meta:
        model = Pharmacy
        fields = [
            "name",
            "category",
            "location",
            "address",
            "start_hour",
            "end_hour",
            "start_day",
            "end_day",
        ]
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'category':forms.TextInput(attrs={'class': 'form-control'}),
            'location':forms.TextInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'start_hour':forms.TimeField(),   
            'end_hour':forms.TimeField(),   
            'start_day':forms.DateField(),   
            'end_day':forms.DateField(),   
        }
