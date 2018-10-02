# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Client(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email = models.EmailField()
    slug = models.SlugField()

class Devis(models.Model):
    DEVIS='Devis'
    FACTURE='Facture'
    PAIEMENT='Payés'
    RELANCE='Relance'
    EN_ATTENTE='En attente'

    TYPE_CHOICES = (
    (DEVIS, "Devis"),
    (FACTURE, "Facture"),
    )
    ETAT_CHOICES =(
    (PAIEMENT, "Payés"),
    (RELANCE, "Relance"),
    (EN_ATTENTE, "En attente"),
    )
    date_de_creation_devis = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default=DEVIS)
    date_de_creation_facture = models.DateTimeField()
    etat = models.CharField(max_length=15, choices=ETAT_CHOICES, default=EN_ATTENTE)

    client = models.ForeignKey(Client, on_delete=models.PROTECT)

class Produit(models.Model):
    nom = models.CharField(max_length=30)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="produits")
    prix = models.DecimalField(max_digits= 8, decimal_places=2)
    stock = models.IntegerField()
    slug = models.SlugField()

class LigneDeCommande(models.Model):
    quantite = models.IntegerField()

    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    devis = models.ForeignKey(Devis, on_delete=models.PROTECT)
