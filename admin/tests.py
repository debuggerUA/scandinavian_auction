# coding: utf-8

from django.test import Client, TestCase
from django.core import mail

class AdminTest(TestCase):
    fixtures = ['testdata.json']
    
    def test_admin_access(self):
        "Here will be admin tests"