from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='categories')
    preview_image=models.ImageField(upload_to='categories/previews')
    desc=models.CharField(max_length=1024)
    
    def __unicode__(self):
        return self.name
    
