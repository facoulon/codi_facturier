# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Client, Produit, Devis, LigneDeCommande
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom', 'email', 'slug')

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom','short_description', 'description', 'slug', 'image', 'prix', 'stock')

class LigneDeCommandeAdmin(admin.ModelAdmin):
    list_display = ('devis','produit', 'quantite')

class DevisAdmin(admin.ModelAdmin):
    list_display = ('client', 'date_de_creation_devis','date_de_modification','type', 'date_de_creation_facture', 'etat')


admin.site.register(Client, ClientAdmin)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(LigneDeCommande, LigneDeCommandeAdmin)
admin.site.register(Devis, DevisAdmin)