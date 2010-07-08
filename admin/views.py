# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from scandinavian_auction.products.forms import ProductForm
from scandinavian_auction.products.models import Product
from scandinavian_auction.auth.forms import LoginForm
from scandinavian_auction.auction.models import Auction, Bids
from scandinavian_auction.auction.forms import AuctionForm
from scandinavian_auction.categories.models import Category
import Image
from django.core.mail import send_mail, EmailMessage
import smtplib
from email.MIMEText import MIMEText
from StringIO import StringIO
from functools import wraps

def superuser_login_required(func):
    @wraps(func)
    def check(request,*args,**kwargs):
        if request.user.is_superuser:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/admin/login')
    return check

#Email notification
def send_notification(params):
    #Notification types: 1-new product, 2-new bid, 3-new category
    email_from = 'debugger88@gmail.com'
    server = 'smtp.gmail.com'
    port = 587
    user_name = 'debugger88@gmail.com'
    user_pass = 'd534fdgg'
    if params['type'] == 1:
        text = "New product added. See at <a href='http://localhost:8000/products/'>http://localhost:8000/products/</a>"
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
        text = "New category added. See at <a href='http://localhost:8000/categories/'>http://localhost:8000/categories/</a>"
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
    

@superuser_login_required
def add_product(request):
    form=ProductForm()
    if request.method=='POST':
        data = request.POST.copy()
        img_file=request.FILES.get('image')
        file_data= {'image':img_file}
        form=ProductForm(data,file_data)
        if form.is_valid():
            simple_upload_file=SimpleUploadedFile(img_file.name,img_file.read())
            img_file.seek(0)
            img=Image.open(img_file)
            img.thumbnail((128, 128))
            outfile = StringIO()
            img.save(outfile,format="JPEG")
            product=Product(name=data['name'],category=Category.objects.get(id=data['category']), cost=data['cost'],desc=data['desc'],image=simple_upload_file,preview_image=SimpleUploadedFile(img_file.name,outfile.getvalue()))
            outfile.close()
            product.save()
            #creating notification email
            params = {'pr_name': product.name, 'to': 'debuggerUA@yandex.ru', 'type': 1}
            send_notification(params)
            return HttpResponseRedirect('/admin/products/')
    return render_to_response('admin/product_form.html',{'product_form':form,'edit':False},context_instance=RequestContext(request))

@superuser_login_required
def get_products(request):
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
    return render_to_response('admin/products.html',{'products':products},context_instance=RequestContext(request))

@superuser_login_required
def get_product(request,id):
    p=Product.objects.get(id=id)
    return render_to_response('admin/product.html',{'product':p},context_instance=RequestContext(request))

@superuser_login_required
def del_product(request,id):
    Product.objects.get(id=id).delete()
    return HttpResponseRedirect('/admin/products/')

@superuser_login_required
def edit_product(request,id):
    product=Product.objects.get(id=id)
    form=ProductForm(instance=product)
    if request.method=='POST':
        data = request.POST.copy()
        img_file=request.FILES.get('image')
        file_data= {'image':img_file}
        print data
        
        form=ProductForm(data,file_data)
        if form.is_valid():
            simple_upload_file=SimpleUploadedFile(img_file.name,img_file.read())
            img_file.seek(0)
            img=Image.open(img_file)
            img.thumbnail((128, 128))
            outfile = StringIO()
            img.save(outfile,format="JPEG")
            product.name=data['name']
            product.cost=data['cost']
            product.desc=data['desc']
            product.image=simple_upload_file
            product.preview_image=SimpleUploadedFile(img_file.name,outfile.getvalue())
            outfile.close()
            product.save()
            return HttpResponseRedirect('/admin/products/')
    return render_to_response('admin/product_form.html',{'product_form':form,'edit':True,'id':id},context_instance=RequestContext(request))

@superuser_login_required
def add_auction(request):
    form=AuctionForm()
    if request.method=='POST':
        data = request.POST.copy()
        form=AuctionForm(data)
        if form.is_valid():
            auction=Auction(start_time=data['start_time'],duration=data['duration'],product=Product.objects.get(id=int(data['product'])),start_price=data['start_price'])
            auction.save()
            return HttpResponseRedirect('/admin/auctions/')
    return render_to_response('admin/auction_form.html',{'auction_form':form,'edit':False},context_instance=RequestContext(request))

@superuser_login_required
def get_auctions(request):
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
    return render_to_response('admin/auctions.html',{'auctions':auctions},context_instance=RequestContext(request))

@superuser_login_required
def del_auction(request,id):
    Product.objects.get(id=id).delete()
    return HttpResponseRedirect('/admin/auctions/')

@superuser_login_required
def edit_auction(request,id):
    product=Product.objects.get(id=id)
    form=ProductForm(instance=product)
    if request.method=='POST':
        data = request.POST.copy()
        img_file=request.FILES.get('image')
        file_data= {'image':img_file}
        print data
        
        form=ProductForm(data,file_data)
        if form.is_valid():
            simple_upload_file=SimpleUploadedFile(img_file.name,img_file.read())
            img_file.seek(0)
            img=Image.open(img_file)
            img.thumbnail((128, 128))
            outfile = StringIO()
            img.save(outfile,format="JPEG")
            product.name=data['name']
            product.cost=data['cost']
            product.desc=data['desc']
            product.image=simple_upload_file
            product.preview_image=SimpleUploadedFile(img_file.name,outfile.getvalue())
            outfile.close()
            product.save()
            return HttpResponseRedirect('/admin/products/')
    return render_to_response('admin/product_form.html',{'product_form':form,'edit':True,'id':id},context_instance=RequestContext(request))


@superuser_login_required
def get_users(request):
    users=User.objects.all()
    return render_to_response('admin/users.html',{'users':users},context_instance=RequestContext(request))

@superuser_login_required
def del_user(request,id):
    User.objects.get(id=id).delete()
    return HttpResponseRedirect('/admin/users/')
    

def admin_login(request):
    form=LoginForm()
    errors={}
    if request.method=='POST':
        data = request.POST.copy()
        form=LoginForm(data)
        if form.is_valid():
            login = request.POST['login']
            password = request.POST['password']
            user = auth.authenticate(username=login, password=password)
            if user is not None and user.is_active and user.is_superuser:
                auth.login(request, user)
                return HttpResponseRedirect("/admin/")
    return render_to_response('admin/login_form.html',{'form':form,'errors':errors},context_instance=RequestContext(request))

@superuser_login_required
def admin_main(request):
    return render_to_response('admin/main.html',{},context_instance=RequestContext(request))

