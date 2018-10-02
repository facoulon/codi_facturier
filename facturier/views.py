# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from .models import Client, Produit, Devis, LigneDeCommande
from django.urls import reverse

# Create your views here.
class IndexView(TemplateView):
    template_name = "facturier/index.html"
    