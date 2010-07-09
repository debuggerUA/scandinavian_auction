from django import forms
from django.forms import ModelForm, Textarea
from scandinavian_auction.auction.models import Auction
from django.forms.extras.widgets import SelectDateWidget


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['start_time', 'time_left', 'price', 'product', 'price_delta']
        widgets = {
            'start_time': SelectDateWidget(),
        }