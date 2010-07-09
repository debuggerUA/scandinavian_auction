from django import forms
from django.forms import ModelForm, Textarea
from scandinavian_auction.categories.models import Category

class CategoryForm(ModelForm):
    desc = forms.CharField(widget=Textarea())
    class Meta:
        model = Category
        fields = ['name','desc','image']