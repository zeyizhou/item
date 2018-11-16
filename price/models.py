from django.db import models

# Create your models here.
from django.db import models
import datetime
from django.utils import timezone

from django.dispatch import receiver
import os
import time

class  Item(models.Model):
    mark = models.CharField('Mark', max_length=200, blank=True)
    name = models.CharField('Name', max_length=200, blank=True)
    fr_price = models.IntegerField ('Franch Price', default=0, blank=True)
    cn_price = models.IntegerField ('China Price', default=0, blank=True)
    sale_price = models.IntegerField('sale Price', default=0, blank=True)
    promo_price = models.IntegerField('promo Price', default=0, blank=True)
    quantity = models.IntegerField('Quantity', default=0, blank=True)
    sold_quantity = models.IntegerField('Sold Quantity', default=0, blank=True)
    image = models.ImageField('image', blank=True, upload_to='Images')

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


@receiver(models.signals.post_delete, sender=Item)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver (models.signals.pre_save, sender=Item)
def auto_delete_file_on_change(sender, instance, *args, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = None
        if(Item.objects.get (pk=instance.pk).image):
            old_image = Item.objects.get (pk=instance.pk).image
        else:
            return False
        print(old_image.path)
    except Item.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile (old_image.path):
            os.remove (old_image.path)
