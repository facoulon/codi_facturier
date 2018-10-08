# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, ListView, TemplateView, CreateView
from django.views.generic import DetailView, UpdateView, DeleteView

from .models import Customer, Product, Quotation, CommandLine

from extra_views import CreateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet

from django.db.models.signals import post_save
from django.db.models import Q


# Create your views here.
class IndexView(TemplateView):
    template_name = "facturier/index.html"

class CustomerCreateView(CreateView):
    model = Customer
    fields = "__all__"
    success_url = '/'

    def get_success_url(self):
        return reverse('customer-detail', args=[self.object.slug] )

class CustomerList(ListView):
    model = Customer
    template_name='facturier/customer_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q',None)

        if query != None:
            return Customer.objects.filter(Q(last_name__icontains=query)|Q(first_name__icontains=query))
            
            #filter
        else:
            return Customer.objects.all()

class CustomerDetail(DetailView):
    model = Customer

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = "__all__"
    template_name = 'facturier/customer_edit.html'

    def get_success_url(self):
        return reverse('customer-detail', args=[self.object.slug] )

class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = '/'
    # template_name = ".html"

class ProductCreateView(CreateView):
    model = Product
    fields = "__all__"
    success_url = '/'

class ProductDetailView(DetailView):
    model = Product

class ProductUpdateView(UpdateView):
    model = Product
    fields = "__all__"
    template_name = 'facturier/product_edit.html'

    def get_success_url(self):
        return reverse('product-detail', args=[self.object.slug] )

class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/'

class ProductListView(ListView):
    model = Product
    template_name='facturier/product_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q',None)

        if query != None:
            return Product.objects.filter(name__icontains=query)
            #filter
        else:
            return Product.objects.all()

class CommandLineInline(InlineFormSet):
    model = CommandLine
    fields = "__all__"

class QuotationCreateView(CreateWithInlinesView):
    model = Quotation
    inlines = [CommandLineInline,]
    fields = ("customer","type","status",)
    template_name = 'facturier/quotation_form.html'
    success_url = '/'

class QuotationListView(ListView):
    model = Quotation

    def get_queryset(self):
        query = self.request.GET.get('q',None)
        query
        if query != None:
            return Quotation.objects.filter(Q(customer__last_name__icontains=query)|Q(customer__first_name__icontains=query))
            #filter
        else:
            return Quotation.objects.all()