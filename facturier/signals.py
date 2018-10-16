from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from .models import Quotation

@receiver(post_save, sender=Quotation)
def bill_creation(sender,instance, **kwargs):
    print "plop"
    if instance.bill_creation_date == None and instance.type == "BILL":
        instance.bill_creation_date = datetime.now()
        instance.save()
