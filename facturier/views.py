# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import post_save
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import View, ListView, TemplateView, CreateView
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string, get_template
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import QuotationForm
from .models import Customer, Product, Quotation, CommandLine
from .models import ETAT_CHOICES


from django_weasyprint import WeasyTemplateResponseMixin
from extra_views import CreateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet

register = template.Library()

# Create your views here.
class IndexView(TemplateView):
    template_name = "facturier/index.html"

class CustomerCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'facturier.add_customer'
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

class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'facturier.change_customer'
    model = Customer
    fields = "__all__"
    template_name = 'facturier/customer_edit.html'

    def get_success_url(self):
        return reverse('customer-detail', args=[self.object.slug] )

class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'facturier.delete_customer'
    model = Customer
    success_url = '/'
    # template_name = ".html"

class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'facturier.add_product'
    model = Product
    fields = "__all__"
    success_url = '/'

class ProductDetailView(DetailView):
    model = Product

class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'facturier.change_product'
    model = Product
    fields = "__all__"
    template_name = 'facturier/product_edit.html'

    def get_success_url(self):
        return reverse('product-detail', args=[self.object.slug] )

class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'facturier.delete_product'
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

class QuotationCreateView(PermissionRequiredMixin, CreateWithInlinesView):
    permission_required = 'facturier.add_quotation'
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
        query3 = self.kwargs['type'].upper()
        if query != None:
            if query2 != "":
                return Quotation.objects.filter(Q(customer__last_name__icontains=query)|Q(customer__first_name__icontains=query), Q(status__icontains=query2), Q(type=query3))
            else:
                return Quotation.objects.filter(Q(customer__last_name__icontains=query)|Q(customer__first_name__icontains=query), Q(type=query3))
            #filter
        else:
            return Quotation.objects.filter(type=query3)

@method_decorator(csrf_exempt, name='dispatch')
class QuotationDetailView(DetailView):
    model = Quotation
    form_class = QuotationForm

    def get_queryset(self):
        query = self.kwargs['type'].upper()
        return Quotation.objects.filter(type=query)

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        context['products'] = Product.objects.all().order_by('name')
        context['pdf'] = False
        context['form'] = QuotationForm
        allLine = CommandLine.objects.filter(quotation=self.object.id)
        total = 0
        for line in allLine:
            total += line.product.price*line.quantity
        context['total'] = total
        return context

@method_decorator(csrf_exempt, name='dispatch')
class UpdateQuotationTypeView(PermissionRequiredMixin, View):
    permission_required = 'facturier.change_quotation'
    def post(self, request):
        quotation = Quotation.objects.get(id = request.POST.get("pk"))
        setattr(quotation, 'type', 'BILL')
        quotation.save()
        return JsonResponse({"redirect_url":reverse( "detail", args=["bill", quotation.id])})

@method_decorator(csrf_exempt, name='dispatch')
class UpdateCommandLineLineView(PermissionRequiredMixin, View):
    permission_required = 'facturier.change_quotation'
    def post(self, request):
        commandline = CommandLine.objects.get(id = request.POST.get("pk"))
        setattr(commandline,request.POST.get("name"), request.POST.get("value"))
        commandline.save()
        return HttpResponse({'success' : True})


@method_decorator(csrf_exempt, name='dispatch')
class DeleteCommandLineLineView(PermissionRequiredMixin, View):
    permission_required = 'facturier.delete_commandline'
    def post(self, request):
        commandline = CommandLine.objects.get(pk = request.POST.get("pk"))
        commandline.delete()
        return HttpResponse({'success' : True})

class QuotationDetailPrintView(WeasyTemplateResponseMixin, QuotationDetailView):

    def get_context_data(self, **kwargs):
        context = QuotationDetailView.get_context_data(self, **kwargs)
        context['pdf'] = True
        return context

    pdf_stylesheets = [
        "facturier/static/css/style.css",
    ]

@method_decorator(csrf_exempt, name='dispatch')
class QuotationAddNewLineView(PermissionRequiredMixin, View):
    permission_required = 'facturier.change_quotation'
    def post(self, request):
        quotation = Quotation.objects.get(id=request.POST.get("quotation-pk"))
        product = Product.objects.get(id=request.POST.get("id-product"))
        quantity = int(request.POST.get('quantity'))

        command_line, created = CommandLine.objects.get_or_create(product = product, quotation=quotation)
        if created == True:
            command_line.quantity = quantity
            command_line.save()
            return JsonResponse({"product_id":command_line.product.id,
                                "product_name":command_line.product.name,
                                "quantity":command_line.quantity,
                                "unit_price":command_line.product.price,
                                "command_line_id":command_line.id           
                                })
        else:
            command_line.quantity += quantity
            command_line.save()
            return JsonResponse({'command_line_id' : command_line.id,
                                'quantity':command_line.quantity,
                                })

import weasyprint
                                

class QuotationSendEmail(PermissionRequiredMixin, View):
    """docstring for QuotationSendEmail."""
    permission_required = 'facturier.change_quotation'

    def get(self, request, pk, type):
        quotation = Quotation.objects.get(id=pk)
        customer = quotation.customer
        # print customer.email


        #generate pdf
        html = render_to_string('facturier/quotation_detail.html', {'quotation': quotation})
        url = reverse('detail', args=[type,pk])
        pdf = weasyprint.HTML(string=html, base_url='url').write_pdf(stylesheets=["facturier/static/css/style.css",])
    
        # send email
        to_email = (customer.email,)
        subject = "Your %s " % quotation.type
        email = EmailMessage(subject, body="vla ton devis", from_email="admin@plop.fr", to=to_email)
        email.attach(quotation.type + "_{}".format(customer.last_name) + '.pdf', pdf, "application/pdf")
        email.content_subtype = "pdf"  # Main content is now text/html
        email.send()
        return HttpResponse({'success' : True})