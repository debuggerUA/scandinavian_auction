from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from scandinavian_auction.products.forms import ProductForm
from scandinavian_auction.products.models import Product
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from StringIO import StringIO
from functools import wraps
from scandinavian_auction.admin.views import send_notification
from scandinavian_auction.auth.forms import LoginForm
from django.contrib import auth
from django.contrib.auth.models import User
from scandinavian_auction.billing.models import Bill  
from scandinavian_auction.auction.models import Auction, Bid
import datetime, time
from django.contrib.auth.decorators import login_required


def show_auctions(request):
    auction_list = Auction.objects.all()
    paginator = Paginator(auction_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        auctions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        auctions = paginator.page(paginator.num_pages)
    return render_to_response('auctions.html',{'auctions':auctions},context_instance=RequestContext(request))

def show_auction(request,id):
    try:
        auction = Auction.objects.get(id=id)
        return render_to_response('auction.html', {'auction': auction}, context_instance=RequestContext(request))
    except Auction.DoesNotExist:
        return HttpResponseRedirect('/auctions/')