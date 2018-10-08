# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Customer, Product, Quotation, CommandLine
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name', 'email', 'city', 'country' , 'cover')
    readonly_fields = ('slug',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','short_description', 'description', 'slug', 'cover', 'price', 'stock')

class CommandLineInline(admin.StackedInline):
    model = CommandLine

class QuotationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'type', 'status',)
    readonly_fields = ("bill_creation_date",)
    inlines = [
        CommandLineInline,
    ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Quotation, QuotationAdmin)