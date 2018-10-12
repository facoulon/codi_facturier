# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, ListView, TemplateView, CreateView
from django.views.generic import DetailView, UpdateView, DeleteView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Customer, Product, Quotation, CommandLine
from .models import ETAT_CHOICES
from django.utils.decorators import method_decorator
from extra_views import CreateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet

from django.views import View

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

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['status'] = ETAT_CHOICES
        return context


    def get_queryset(self):
        query = self.request.GET.get('q',None)
        query2 = self.request.GET.get('filter',None)
        if query != None:
            if query2 != "":
                return Quotation.objects.filter(Q(customer__last_name__icontains=query)|Q(customer__first_name__icontains=query), Q(status__icontains=query2))
            else:
                return Quotation.objects.filter(Q(customer__last_name__icontains=query)|Q(customer__first_name__icontains=query))
            #filter
        else:
            return Quotation.objects.all()

@method_decorator(csrf_exempt, name='dispatch')
class QuotationDetailView(DetailView):
    model = Quotation

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        context['product'] = Product.objects.all()
        return context


@method_decorator(csrf_exempt, name='dispatch')
class UpdateCustomerLineView(View):

    def post(self, request):
        customer = Customer.objects.get(pk = request.POST.get("pk"))
        setattr(customer,request.POST.get("name"),request.POST.get("value"))
        customer.save()
        return HttpResponse({'success' : True})

@method_decorator(csrf_exempt, name='dispatch')
class UpdateCommandLineLineView(View):

    def post(self, request):
        commandline = CommandLine.objects.get(pk = request.POST.get("pk"))
        setattr(commandline,request.POST.get("name"),request.POST.get("value"))
        commandline.save()
        return HttpResponse({'success' : True})
    