# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from autoslug import AutoSlugField
# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 
    slug = AutoSlugField(populate_from='full_name', unique=True, always_update=True)
    email = models.EmailField()
    country = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    cover = models.ImageField(upload_to="customer",blank=True)

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.last_name+" "+self.first_name

TYPE_CHOICES = (
    ("QUOTATION", "Quotation"),
    ("BILL", "Bill"),
)
ETAT_CHOICES =(
    ("PAID", "Paid"),
    ("REVIVE", "Revive"),
    ("WAITING", "En attente"),
)
class Quotation(models.Model):


    quotation_creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    bill_creation_date = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default="QUOTATION")
    status = models.CharField(max_length=15, choices=ETAT_CHOICES, default="WAITING")

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class Product(models.Model):
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from="name")
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    cover = models.ImageField(upload_to="product",blank=True)
    price = models.FloatField()
    stock = models.IntegerField()

    def __unicode__(self):
        return self.name

class CommandLine(models.Model):
    quantity = models.IntegerField()

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)

