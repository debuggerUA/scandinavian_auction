# coding: utf-8

from django.test import Client, TestCase
from django.db import models
from django.contrib.auth.models import User
from scandinavian_auction.categories.models import Category
from scandinavian_auction.products.models import Product
from scandinavian_auction.auction.models import Auction

class AdminTest(TestCase):
    fixtures = ['testdata.json']
    
    def test_admin_access(self):
        "test for admin access"
        print 'starting admin panel access test'
        response = self.client.get('/admin/')
        self.assertRedirects(response, '/admin/login/')
        self.client.post('/registration/', {'login': 'test', 'email': 'test@mail.com', 'password': 'pass', 'confirm_password': 'pass'})
        self.client.post('/login/', {'login': 'test', 'password': 'pass'})
        response = self.client.get('/admin/')
        self.assertRedirects(response, '/admin/login/')
        usr = User.objects.get(username = 'test')
        usr.is_staff = True
        usr.is_superuser = True
        usr.save()
        response = self.client.post('/admin/login/', {'login': 'test', 'password': 'pass'})
        self.assertRedirects(response, '/admin/')
    
    def test_admin_users(self):
        "test for users add/delete/modify in admin panel"
        print 'starting admin panel users test'
        self.client.post('/registration/', {'login': 'test', 'email': 'test@mail.com', 'password': 'pass', 'confirm_password': 'pass'})
        usr = User.objects.get(username = 'test')
        usr.is_staff = True
        usr.is_superuser = True
        usr.save()
        response = self.client.post('/admin/login/', {'login': 'test', 'password': 'pass'})
        response = self.client.get('/admin/')
        self.assertContains(response, 'Administration panel')
        response = self.client.get('/admin/users/')
        self.assertContains(response, 'User list')
        response = self.client.get('/admin/users/add/')
        self.assertContains(response, 'Add user')
        response = self.client.post('/admin/users/add/', {'username': 'tlogin', 'password': 'tpass', 'confirm_password': 'tpass', 'email': 't@mail.com', 'is_staff': False, 'is_active': True, 'is_superuser': False})
        self.assertRedirects(response, '/admin/users/')
        response = self.client.get('/admin/users/')
        self.assertContains(response, 'tlogin')
        self.client.get('/')
        reponse = self.client.get('/logout/')
        response = self.client.get('/')
        self.assertContains(response, 'Welcome, new user.')
        response = self.client.post('/login/', {'login': 'tlogin', 'password': 'tpass'})
        response = self.client.get('/')
        self.assertContains(response, 'Log Out')
        self.client.get('/logout/')
        response = self.client.post('/admin/login/', {'login': 'test', 'password': 'pass'})
        response = self.client.get('/admin/')
        self.assertContains(response, 'Administration panel')
        response = self.client.get('/admin/users/')
        self.assertContains(response, 'User list')
        user = User.objects.get(username = 'tlogin')
        req = '/admin/users/del/' + user.id.__str__() + '/'
        response = self.client.get(req)
        response = self.client.get('/admin/users/')
        self.assertNotContains(response, 'tlogin')
        self.client.get('/logout/')
    
    def test_products(self):
        "products test"
        print 'starting products test'
        self.client.post('/registration/', {'login': 'test', 'email': 'test@mail.com', 'password': 'pass', 'confirm_password': 'pass'})
        usr = User.objects.get(username = 'test')
        usr.is_staff = True
        usr.is_superuser = True
        usr.save()
        response = self.client.post('/admin/login/', {'login': 'test', 'password': 'pass'})
        response = self.client.get('/admin/')
        self.assertContains(response, 'Administration panel')
        f = open('test_media/3.jpg')
        response = self.client.post('/admin/categories/add/', {'name': 'testcat', 'desc': 'hello, world!','image': f})
        f.close()
        response = self.client.get('/admin/categories/')
        self.assertContains(response, 'testcat')
        cat = Category.objects.get(name = 'testcat')
        f = open('test_media/3.jpg')
        response = self.client.post('/admin/products/add/', {'name': 'test_product', 'number': 1, 'category': cat.id, 'cost': 10, 'desc': 'hello, world!', 'image': f})
        f.close()
        response = self.client.get('/admin/products/')
        self.assertContains(response, 'test_product')
        prd = Product.objects.get(name = 'test_product')
        req = '/admin/products/del/' + prd.id.__str__() + '/'
        response = self.client.get(req)
        response = self.client.get('/admin/products/')
        self.assertNotContains(response, 'test_product')
    
    def test_auction(self):
        "auction test"
        print 'starting auction test'
        self.client.post('/registration/', {'login': 'test', 'email': 'test@mail.com', 'password': 'pass', 'confirm_password': 'pass'})
        usr = User.objects.get(username = 'test')
        usr.is_staff = True
        usr.is_superuser = True
        usr.save()
        response = self.client.post('/admin/login/', {'login': 'test', 'password': 'pass'})
        response = self.client.get('/admin/')
        self.assertContains(response, 'Administration panel')
        f = open('test_media/3.jpg')
        response = self.client.post('/admin/categories/add/', {'name': 'testcat', 'desc': 'hello, world!','image': f})
        f.close()
        cat = Category.objects.get(name = 'testcat')
        f = open('test_media/3.jpg')
        response = self.client.post('/admin/products/add/', {'name': 'test_product', 'number': 1, 'category': cat.id, 'cost': 10, 'desc': 'hello, world!', 'image': f})
        f.close()
        prd = Product.objects.get(name = 'test_product')
        response = self.client.post('/admin/auctions/add/', {'time_left': '01:00:00', 'product': prd.id, 'price': 10, 'time_delta': '00:00:20'})
        #print response
        response = self.client.get('/')
        self.assertContains(response, 'test_product')
        response = self.client.get('/admin/auctions/')
        self.assertContains(response, 'test_product')
        prd = Product.objects.get(name = 'test_product')
        auc = Auction.objects.get(product = prd)
        response = self.client.get('/auctions/')
        self.assertContains(response, 'test_product')
        response = self.client.get('/auctions/' + auc.id.__str__() + '/')
        self.assertContains(response, 'Current price:')
        self.client.get('/admin/auctions/del/' + auc.id.__str__() + '/')
        response = self.client.get('/')
        self.assertNotContains(response, 'test_product')