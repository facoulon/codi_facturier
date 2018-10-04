# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Customer, Product, Quotation, CommandLine
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('lastname','firstname', 'email', 'slug', 'city', 'country' , 'cover')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','short_description', 'description', 'slug', 'cover', 'price', 'stock')

class CommandLineAdmin(admin.ModelAdmin):
    list_display = ('quotation','product', 'quantity')

class QuotationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'Quotation_creation_date','modified_date','type', 'Bill_creation_date', 'status')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CommandLine, CommandLineAdmin)
admin.site.register(Quotation, QuotationAdmin)