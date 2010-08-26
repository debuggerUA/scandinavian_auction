# coding: utf-8

from django.test import Client, TestCase
from django.db import models
from django.contrib.auth.models import User
from scandinavian_auction.products.models import Product
from scandinavian_auction.categories.models import Category

class ProductsTest(TestCase):
    fixtures = ['testdata.json']
    
    def test_products_user(self):
        "product test (not admin)"
        print 'starting products test (not admin)'
        self.client.post('/registration/', {'login': 'test', 'email': 'test@mail.com', 'password': 'pass', 'confirm_password': 'pass'})
        usr = User.objects.get(username = 'test')
        usr.is_staff = True
        usr.is_superuser = True
        usr.save()
        response = self.client.post('/admin/login/', {'login': 'test', 'password': 'pass'})
        f = open('test_media/3.jpg')
        response = self.client.post('/admin/categories/add/', {'name': 'testcat', 'desc': 'hello, world!','image': f})
        f.close()
        f = open('test_media/3.jpg')
        cat = Category.objects.get(name = 'testcat')
        response = self.client.post('/admin/products/add/', {'name': 'test_product', 'number': 1, 'category': cat.id, 'cost': 10, 'desc': 'hello, world!', 'image': f})
        f.close()
        self.client.get('/logout/')
        response = self.client.get('/products/')
        self.assertContains(response, 'test_product')
        prd = Product.objects.get(name = 'test_product')
        response = self.client.get('/products/' + prd.id.__str__() + '/')
        self.assertContains(response, 'test_product')
