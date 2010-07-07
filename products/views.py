from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from scandinavian_auction.products.forms import ProductForm
from scandinavian_auction.products.models import Product
from django.template import RequestContext

def products_list(request):
    products = Product.objects.get()
    
    