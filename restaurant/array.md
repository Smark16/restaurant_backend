from django.db import models
from django.contrib.postgres.fields import ArrayField

class Order(models.Model):
    user = models.CharField(max_length=100)
    order_date = models.DateField(auto_now=True)
    names = ArrayField(models.CharField(max_length=100))  # Array of names
    price = models.CharField(max_length=100)
    contact = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=100, default="In Progress")