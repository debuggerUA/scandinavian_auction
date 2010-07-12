from django.shortcuts import render_to_response
from scandinavian_auction.auth.forms import LoginForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth 
from django.contrib.auth.models import User
from scandinavian_auction.auth.forms import RegistrationForm
from scandinavian_auction.billing.models import Bill

def login(request):
    form=LoginForm()
    if request.method=='POST':
        data = request.POST.copy()
        form=LoginForm(data)
        if form.is_valid():
            login = request.POST['login']
            password = request.POST['password']
            user = auth.authenticate(username=login, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
    val=request.user
    return render_to_response('login_form.html',{'form':form,'val':val},context_instance=RequestContext(request))

def registration(request):
    form = RegistrationForm()   
    if request.method == 'POST':
        data = request.POST.copy()
        form = RegistrationForm(data)
        if form.is_valid():
            try:
                user = User.objects.create_user(request.POST.get("login"), request.POST.get('email'), request.POST.get('password'))
                user.save()
                bill = Bill(uid=user, bets=0)
                bill.save()
                return HttpResponseRedirect("/")
            except:
                err_mess = 'This username is unavailable.'
                return render_to_response("registration_form.html", {'form' : form, 'errors': form.errors, 'error_message': err_mess },context_instance=RequestContext(request))
    return render_to_response("registration_form.html", {'form' : form, 'errors': form.errors, },context_instance=RequestContext(request))

def log_out(request):
    #auth.logout(request)
    logout(request)
    return HttpResponseRedirect("/")
    
    