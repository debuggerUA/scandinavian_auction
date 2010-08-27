from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from scandinavian_auction.products.models import Product
from scandinavian_auction.auth.forms import LoginForm
from scandinavian_auction.categories.forms import CategoryForm
from scandinavian_auction.categories.models import Category
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from scandinavian_auction.admin.views import send_notification
from django.core.files.uploadedfile import SimpleUploadedFile
from scandinavian_auction.auth.forms import LoginForm
import Image
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

@superuser_login_required
def categories_list_admin(request):
    categories_list = Category.objects.all()
    paginator = Paginator(categories_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        categories = paginator.page(page)
    except (EmptyPage, InvalidPage):
        categories = paginator.page(paginator.num_pages)
    return render_to_response('admin/categories.html',{'categories':categories},context_instance=RequestContext(request))

@superuser_login_required
def category_show_admin(request,id):
    cat = Category.objects.get(id=id)
    return render_to_response('admin/category.html', {'category': cat}, context_instance=RequestContext(request))

def show_category(request,id):
    cat = Category.objects.get(id=id)
    products_list = Product.objects.filter(category=cat)
    paginator = Paginator(products_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render_to_response('category.html', {'category': cat, 'products': products}, context_instance=RequestContext(request))

def show_categories(request):
    categories_list = Category.objects.all()
    paginator = Paginator(categories_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        categories = paginator.page(page)
    except (EmptyPage, InvalidPage):
        categories = paginator.page(paginator.num_pages)
    return render_to_response('categories.html', {'categories':categories},context_instance=RequestContext(request))

@superuser_login_required
def add_category(request):
    form=CategoryForm()
    if request.method=='POST':
        data = request.POST.copy()
        img_file=request.FILES.get('image')
        file_data= {'image':img_file}
        form=CategoryForm(data,file_data)
        if form.is_valid():
            simple_upload_file=SimpleUploadedFile(img_file.name,img_file.read())
            img_file.seek(0)
            img=Image.open(img_file)
            img.thumbnail((128, 128))
            outfile = StringIO()
            img.save(outfile,format="JPEG")
            category=Category(name=data['name'],desc=data['desc'],image=simple_upload_file,preview_image=SimpleUploadedFile(img_file.name,outfile.getvalue()))
            outfile.close()
            category.save()
            #creating notification email
            params = {'pr_name': category.name, 'to': 'debuggerUA@yandex.ru', 'type': 3}
            send_notification(params)
            return HttpResponseRedirect('/admin/categories/')
    return render_to_response('admin/category_form.html',{'category_form':form,'edit':False},context_instance=RequestContext(request))

@superuser_login_required
def del_category(request,id):
    Category.objects.get(id=id).delete()
    return HttpResponseRedirect('/admin/categories/')
