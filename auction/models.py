# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from scandinavian_auction.products.models import Product

class Bid(models.Model):
    user=models.ForeignKey(User)
    time=models.DateTimeField()
    class Meta:
        get_latest_by = 'time'

class Auction(models.Model):
    #start_time=models.DateTimeField()
    time_left=models.TimeField()
    price=models.FloatField()
    product=models.ForeignKey(Product)
    bids=models.ManyToManyField(Bid)
    time_delta=models.TimeField()
    class Meta:
        get_latest_by = 'id'