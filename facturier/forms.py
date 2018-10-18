from django.forms import ModelForm
from .models import Quotation
from django.db import models
from django import forms

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ('type',)