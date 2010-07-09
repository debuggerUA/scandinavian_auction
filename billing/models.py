# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Bill(models.Model):
    uid=models.ForeignKey(User)
    balance=models.FloatField()
