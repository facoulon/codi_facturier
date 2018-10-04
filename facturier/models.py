# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Customer(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    email = models.EmailField()
    country = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    cover = models.ImageField(upload_to="customer",blank=True)
    slug = models.SlugField()

    def __unicode__(self):
        return self.lastname+" "+self.firstname

class Quotation(models.Model):

    TYPE_CHOICES = (
        ("QUOTATION", "Quotation"),
        ("BILL", "Bill"),
    )
    ETAT_CHOICES =(
        ("PAIEMENT", "PayPaidés"),
        ("REVIVE", "Revive"),
        ("WAITING", "Waiting"),
    )

    Quotation_creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default="QUOTATION")
    Bill_creation_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=ETAT_CHOICES, default="WAITING")

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class Product(models.Model):
    name = models.CharField(max_length=30)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    cover = models.ImageField(upload_to="product")
    price = models.DecimalField(max_digits= 8, decimal_places=2)
    stock = models.IntegerField()
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

class CommandLine(models.Model):
    quantity = models.IntegerField()

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quotation = models.ForeignKey(Quotation, on_delete=models.PROTECT)
