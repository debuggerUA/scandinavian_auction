from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from scandinavian_auction.auction.models import Auction


def main(request):
    auctions=Auction.objects.filter(is_active=True)
    return render_to_response('home.html',{'auctions':auctions},context_instance=RequestContext(request))


