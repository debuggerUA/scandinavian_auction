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
    duration=models.TimeField()
    start_price=models.FloatField()
    product=models.ForeignKey(Product)
    bids=models.ManyToManyField(Bids)
    class Meta:
        get_latest_by = 'id'