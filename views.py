from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from scandinavian_auction.auction.models import Auction
import datetime, time
from django.utils import simplejson


def main(request):
    auctions=Auction.objects.filter(is_active=True)
    return render_to_response('home.html',{'auctions':auctions},context_instance=RequestContext(request))

def aj_update_main(request):
    auctions=Auction.objects.filter(is_active=True)
    id_hash_sum = 0
    time_left_array = []
    prices_array = []
    products_array = []
    for auction in auctions:
        id_hash_sum += auction.id
        time_left_array.append(auction.time_left.__str__())
        prices_array.append(auction.price)
        products_array.append(auction.product.name)
    data = {}
    data.update({'id_hash_sum': id_hash_sum, 'products_array': products_array, 'time_left_array': time_left_array, 'prices_array': prices_array, 'success': True})
    return HttpResponse(simplejson.dumps(data))

#Email notification
def send_notification(params):
    #Notification types: 1-new product, 2-new bid, 3-new category, 4-auction won
    email_from = 'debugger88@gmail.com'
    server = 'smtp.gmail.com'
    port = 587
    user_name = 'debugger88@gmail.com'
    user_pass = 'd534fdgg'
    if params['type'] == 1:
        text = "New product added."
        subj = 'New product at auction!'
        msg = MIMEText(text, "", "utf-8")
        msg['Subject'] = subj
        msg['From'] = email_from
        msg['To'] = params['to']
        s = smtplib.SMTP(server, port)
        s.starttls()
        s.login(user_name, user_pass)
        s.sendmail(email_from, params['to'], msg.as_string())
        s.quit()
    if params['type'] == 3:
        text = "New category added."
        subj = 'New category!'
        msg = MIMEText(text, "", "utf-8")
        msg['Subject'] = subj
        msg['From'] = email_from
        msg['To'] = params['to']
        s = smtplib.SMTP(server, port)
        s.starttls()
        s.login(user_name, user_pass)
        s.sendmail(email_from, params['to'], msg.as_string())
        s.quit()
    if params['type'] == 4:
        text = "Congratulations! You've won!"
        subj = 'gz'
        msg = MIMEText(text, "", "utf-8")
        msg['Subject'] = subj
        msg['From'] = email_from
        msg['To'] = params['to']
        s = smtplib.SMTP(server, port)
        s.starttls()
        s.login(user_name, user_pass)
        s.sendmail(email_from, params['to'], msg.as_string())
        s.quit()