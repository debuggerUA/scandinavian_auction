# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from scandinavian_auction.products.models import Product


class Auction(models.Model):
    time_left=models.TimeField()
    price=models.FloatField()
    product=models.ForeignKey(Product)
    time_delta=models.TimeField()
    class Meta:
        get_latest_by = 'id'


class Bid(models.Model):
    user=models.ForeignKey(User)
    time=models.DateTimeField()
    auction=models.ForeignKey(Auction)
    class Meta:
        get_latest_by = 'time'