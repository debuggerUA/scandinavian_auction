# coding: utf-8

from django.test import Client, TestCase
from django.core import mail
from django.db import models
from django.contrib.auth.models import User
from scandinavian_auction.categories.models import Category

class AdminTest(TestCase):
    fixtures = ['testdata.json']
    
    def test_admin_access(self):
        "test for admin access"
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
        response = self.client.get('/admin/users/del/3/')
        response = self.client.get('/admin/users/')
        self.assertNotContains(response, 'tlogin')
        self.client.get('/logout/')
    
    def products_test(self):
        self.client.post('/registration/', {'login': 'test', 'email': 'test@mail.com', 'password': 'pass', 'confirm_password': 'pass'})
        usr = User.objects.get(username = 'test')
        usr.is_staff = True
        usr.is_superuser = True
        usr.save()
        response = self.client.post('/admin/login/', {'login': 'test', 'password': 'pass'})
        response = self.client.get('/admin/')
        self.assertContains(response, 'Administration panel')
        f = open('media/categories/3.jpg')
        response = self.client.post('/admin/categories/add/', {'name': 'testcat', 'desc': 'hello, world!','image': f})
        #f.close()
        response = self.client.get('/admin/categories/')
        self.assertContains(response, 'testcat')
        cat = Category.objects.get(name = 'testcat')
        response = self.client.post('/admin/products/add/', {'name': 'test_product', 'number': 1, 'category': cat.id, 'cost': 10, 'desc': 'hello, world!', 'image': f})
        f.close()
        response = self.client.get('/admin/products/')
        self.assertContains(response, 'test_product')
        response = self.client.get('/admin/products/del/1/')
        response = self.client.get('/admin/products/')
        self.assertNotContains(response, 'test_product')
    