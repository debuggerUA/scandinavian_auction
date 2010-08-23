# coding: utf-8

from django.test import Client, TestCase
from django.core import mail

class ClientTest(TestCase):
    fixtures = ['testdata.json']
    
    def test_registration_login_logout(self):
        response = self.client.get('/')
        self.assertContains(response, 'log in.')
        response = self.client.get('/registration/')
        self.assertContains(response, 'Login:')
        self.assertContains(response, 'Password:')
        response = self.client.post('/registration/', {'login': 'test', 'email': 'test@mail.com', 'password': 'pass', 'confirm_password': 'pass'})
        self.client.get('/')
        response = self.client.get('/login/')
        self.assertContains(response, 'Authorization')
        self.client.post('/login/', {'login': 'test', 'password': 'pass'})
        response = self.client.get('/')
        self.assertContains(response, 'Log Out')
        self.client.get('/logout/')
        response = self.client.get('/')
        self.assertContains(response, 'Welcome, new user.')