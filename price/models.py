from django.db import models

# Create your models here.
from django.db import models
import datetime
from django.utils import timezone
from django import forms
import time


class  Item(models.Model):
    mark = models.CharField('Mark', max_length=200, blank=True)
    name = models.CharField('Name', max_length=200, blank=True)
    price = models.IntegerField('Price', default=0, blank=True)
    quantity = models.IntegerField('Quantity', default=0, blank=True)
    sold_quantity = models.IntegerField('Sold Quantity', default=0, blank=True)
    pub_date = models.DateField('date added', blank=True, default=str(time.strftime ('%Y-%m-%d', time.localtime (time.time ()))))

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
