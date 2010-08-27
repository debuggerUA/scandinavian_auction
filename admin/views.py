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
from scandinavian_auction.auction.models import Auction, Bid
from scandinavian_auction.auction.forms import AuctionForm
from scandinavian_auction.auth.forms import AdminAddUserForm
from scandinavian_auction.categories.models import Category
from scandinavian_auction.billing.models import Bill
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
            return HttpResponseRedirect('/admin/login/')
    return check

#Email notification - ПЕРЕПИСАТЬ НАФИК!11!1
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
            product=Product(name=data['name'], number=data['number'], category=Category.objects.get(id=data['category']), cost=data['cost'],desc=data['desc'],image=simple_upload_file,preview_image=SimpleUploadedFile(img_file.name,outfile.getvalue()))
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
    try:
        p=Product.objects.get(id=id)
        auc = Auction.objects.filter(is_active=True, product=p)
        return render_to_response('admin/product.html',{'product':p},context_instance=RequestContext(request))
    except DoesNotExist:
        return HttpResponseRedirect('/')

@superuser_login_required
def del_product(request,id):
    try:
        Product.objects.get(id=id).delete()
    except Product.DoesNotExist:
        pass
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
            product.number=data['number']
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
            auction=Auction(time_left=data['time_left'], product=Product.objects.get(id=int(data['product'])), price=data['price'], time_delta=data['time_delta'], is_active=True)
            prod=Product.objects.get(id=int(data['product']))
            if prod.number > 0:
                prod.number -= 1
                prod.save()
            else:
                pass
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
    try:
        Auction.objects.get(id=id).delete()
    except Auction.DoesNotExist:
        pass
    return HttpResponseRedirect('/admin/auctions/')

@superuser_login_required
def edit_auction(request,id):
    auction=Auction.objects.get(id=id)
    form=AuctionForm(instance=auction)
    if request.method=='POST':
        data = request.POST.copy()      
        form=AuctionForm(data,file_data)
        if form.is_valid():
            auction.time_left=data['time_left']
            auction.price=data['price']
            auction.product=data['product']
            auction.time_delta=data['time_delta']
            auction.save()
            return HttpResponseRedirect('/admin/auctions/')
    return render_to_response('admin/auction_form.html',{'auction_form':form,'edit':True,'id':id},context_instance=RequestContext(request))


@superuser_login_required
def get_users(request):
    users=User.objects.all()
    return render_to_response('admin/users.html',{'users':users},context_instance=RequestContext(request))

@superuser_login_required
def del_user(request,id):
    try:
        User.objects.get(id=id).delete()
    except User.DoesNotExist:
        pass
    return HttpResponseRedirect('/admin/users/')

def add_user(request):
    form = AdminAddUserForm()
    if request.method == 'POST':
        data = request.POST.copy()
        form = AdminAddUserForm(data)
        if form.is_valid():
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            try:
                user.is_superuser = data['is_superuser']
            except:
                user.is_superuser = False
            try:
                user.is_staff = data['is_staff']
            except:
                user.is_staff = False
            try:
                user.is_active = data['is_active']
            except:
                user.is_active = False
            user.save()
            return HttpResponseRedirect("/admin/users/")
    return render_to_response('admin/user_form.html', {'user_form': form, 'edit': False}, context_instance=RequestContext(request))
    

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

def user_page(request):
    if request.user.is_authenticated():
        usr = User.objects.get(id=request.user.id)
        bill = Bill.objects.get(uid=usr.id)
        mybids = Bid.objects.filter(user=request.user.id)
        bids_auc_id = [] #список ID аукционов, в которых принимал участие
        for bid in mybids:
            if bid.auction.id not in bids_auc_id:
                bids_auc_id.append(bid.auction.id)
        u_bids = [] #список АУКЦИОНОВ
        for id in bids_auc_id:
            au = Auction.objects.get(id = id)
            u_bids.append(au)
        print u_bids 
        auct_won = Auction.objects.filter(won_by = usr.id, is_active = True)
        return render_to_response('user.html', {'user': usr, 'bill': bill, 'bids': u_bids, 'auc_won': auct_won}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/')

def buy_it(request, id):
    try:
        auc = Auction.objects.get(id=id)
    except DoesNotExist:
        return HttpResponseRedirect('/')
    if auc.won_by.id == request.user.id:
        #Биллинг и всё такое :)
        #будем считать, что купили успешно
        auc_bids = Bid.objects.filter(auction=auc).delete()
        auc.delete()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/user/')