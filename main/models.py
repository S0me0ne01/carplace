from django.db import models

from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.shortcuts import get_object_or_404
from django.http import Http404

from django.db.models.signals import pre_save, post_save, post_init
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

import datetime


class Offer(models.Model):
    name = models.CharField(max_length = 100)
    name_kz = models.CharField(max_length = 100, null = True, blank = True)
    description = models.CharField(max_length = 1000, null = True, blank = True)
    description_kz = models.CharField(max_length = 1000, null = True, blank = True)
    price = models.PositiveIntegerField()
    views = models.PositiveIntegerField(default = 0)

    published = models.DateTimeField(auto_now_add = True)

    class Meta:
        abstract = True


class Product(Offer):
    category = models.ForeignKey('ProductCategory', related_name = 'category', on_delete = models.CASCADE)
    in_stock = models.BooleanField()

    def __str__(self):
        return self.name


class Service(Offer):
    category = models.ForeignKey('ServiceCategory', related_name = 'category', on_delete = models.CASCADE)
    duration = models.CharField(max_length = 50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length = 100)
    name_kz = models.CharField(max_length = 100, null = True, blank = True)
    image = models.ImageField(verbose_name = 'Изображение', null = True)

    class Meta:
        abstract = True

class ProductCategory(Category):

    def __str__(self):
        return self.name

class ServiceCategory(Category):

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(User, related_name = 'client', on_delete = models.CASCADE)

@receiver(post_save, sender=User)
def user_create(sender, instance, created, **kwargs):
	if created:
		Client.objects.create(user=instance)


class Phone(models.Model):
    phone = models.CharField(max_length=12, validators=[MinLengthValidator(11)])

    def __str__(self):
        return self.phone


class Ip(models.Model):
    adress = models.CharField(max_length = 50)
    year = models.CharField(max_length = 50)
    month = models.CharField(max_length = 50)
    viewed_products = models.ManyToManyField('Product', through = "ProductView")
    viewed_services = models.ManyToManyField('Service', through = "ServiceView")


class ProductView(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE)
    ip = models.ForeignKey('Ip', on_delete = models.CASCADE)

class ServiceView(models.Model):
    service = models.ForeignKey('Service', on_delete = models.CASCADE)
    ip = models.ForeignKey('Ip', on_delete = models.CASCADE)


class Search(models.Model):
    text = models.CharField(max_length = 100)
