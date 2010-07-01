from django.db import models


class Product(models.Model):
    name=models.CharField(max_length=100)
    cost=models.FloatField()
    desc=models.CharField(max_length=1024)
    image=models.ImageField(upload_to='products')
    preview_image=models.ImageField(upload_to='products/previews')
    
    class Meta:
        get_latest_by = 'id'
        
    def __unicode__(self):
        return self.name
