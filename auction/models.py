# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from scandinavian_auction.products.models import Product

class Bids(models.Model):
    user=models.ForeignKey(User)
    time=models.DateTimeField()
    class Meta:
        get_latest_by = 'time'

class Auction(models.Model):
    start_time=models.DateTimeField()
    time_left=models.TimeField()
    price=models.FloatField()
    product=models.ForeignKey(Product)
    bids=models.ManyToManyField(Bids)
    price_delta=models.FloatField()
    class Meta:
        get_latest_by = 'id'