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


def user_login_required(func):
    @wraps(func)
    def check(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login')
    return check

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

def show_product(request,id):
    p=Product.objects.get(id=id)
    return render_to_response('product_form.html',{'product':p},context_instance=RequestContext(request))

@user_login_required
def make_bid(request,id):
    user = User.objects.get(id=request.user.id)
    bill = Bill.objects.get(uid=user.id)
    auction = Auction.objects.get(id=id)
    if bill.bets > 0:
        bid = Bid(user=user, time=datetime.datetime.now())
        bid.save()
        secs = auction.time_left.hour*3600 + auction.time_left.minute*60 + auction.time_left.second
        secs_delta = auction.time_delta.second
        secs += secs_delta
        auction.time_left = datetime.time(secs/3600, (secs % 3600)/60, secs % 60)
        auction.price += 0.25
        auction.save()
        bill.bets -= 1
        bill.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
