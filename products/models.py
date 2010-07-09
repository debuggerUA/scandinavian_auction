from django.db import models
from scandinavian_auction.categories.models import Category


class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category)
    cost=models.FloatField()
    number=models.IntegerField()
    desc=models.CharField(max_length=1024)
    image=models.ImageField(upload_to='products')
    preview_image=models.ImageField(upload_to='products/previews')
    
    class Meta:
        get_latest_by = 'id'
        
    def __unicode__(self):
        return self.name
