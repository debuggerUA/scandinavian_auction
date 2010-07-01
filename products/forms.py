from django import forms
from django.forms import ModelForm, Textarea
from scandinavian_auction.products.models import Product

class ProductForm(ModelForm):
    desc = forms.CharField(widget=Textarea())
    class Meta:
        model = Product
        fields = ['name', 'cost', 'desc','image']