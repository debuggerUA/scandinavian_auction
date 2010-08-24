from django.test import Client, TestCase
from django.core import mail
from django.db import models
from django.contrib.auth.models import User
from scandinavian_auction.categories.models import Category

class CategoryTest(TestCase):
    fixtures = ['testdata.json']
    
    def test_categories(self):
        "categories test"
        self.client.post('/registration/', {'login': 'test', 'email': 'test@mail.com', 'password': 'pass', 'confirm_password': 'pass'})
        usr = User.objects.get(username = 'test')
        usr.is_staff = True
        usr.is_superuser = True
        usr.save()
        response = self.client.post('/admin/login/', {'login': 'test', 'password': 'pass'})
        response = self.client.get('/admin/')
        self.assertContains(response, 'Administration panel')
        response = self.client.get('/admin/categories/')
        self.assertContains(response, 'Categories list')
        response = self.client.get('/admin/categories/add/')
        self.assertContains(response, 'Add Category')
        f = open('media/categories/3.jpg')
        response = self.client.post('/admin/categories/add/', {'name': 'testcat', 'desc': 'hello, world!','image': f})
        f.close()
        response = self.client.get('/admin/categories/')
        self.assertContains(response, 'testcat')
        response = self.client.get('/admin/categories/1/')
        self.assertContains(response, 'hello, world!')
        response = self.client.get('/admin/categories/del/1/')
        response = self.client.get('/admin/categories/')
        self.assertNotContains(response, 'testcat')