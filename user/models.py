from decouple import config, Csv
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from multiprocessing import Process
from space.models import *



class Kart(models.Model):
    product = models.ManyToManyField(Product, related_name='px')

    def __str__(self):
        return f'{self.pk} cart'


class Order(models.Model):
    cart = models.ForeignKey(Kart, related_name="kx",
                             on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk} Order'



