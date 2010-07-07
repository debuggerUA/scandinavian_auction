from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from scandinavian_auction.products.forms import ProductForm
from scandinavian_auction.products.models import Product
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def products_list(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render_to_response('products.html',{'products':products},context_instance=RequestContext(request))
    
    