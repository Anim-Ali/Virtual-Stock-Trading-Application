from django.db import models
import pandas as pd
import time
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=8, decimal_places=2, default=10000.00, blank=False)
    # funds = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# This may be useless as Group by can be used in transaction table to get index
"""
class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolio")
    symbol = models.CharField(max_length=5, blank=False)
    name = models.CharField(max_length=90, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    shares = models.IntegerField()
"""

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    symbol = models.CharField(max_length=5, blank=False)
    name = models.CharField(max_length=90, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    shares = models.IntegerField()
    date = models.DateTimeField(null=False, blank=False)

