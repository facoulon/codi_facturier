# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView, CreateView
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Customer, Product, Quotation, CommandLine
from django.urls import reverse

# Create your views here.
class IndexView(TemplateView):
    template_name = "facturier/index.html"

class CustomerCreateView(CreateView):
    model = Customer
    fields = "__all__"
    success_url = '/index'

    def get_success_url(self):
        return reverse('customer-detail', args=[self.object.slug] )
    
class CustomerList(ListView):
    model = Customer
    template_name='facturier/customer_list.html'

class CustomerDetail(DetailView):
    model = Customer

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = "__all__"
    template_name = 'facturier/customer_edit.html'

class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = '/index'
    # template_name = ".html"
