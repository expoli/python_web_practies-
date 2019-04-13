from django.db import models

# Create your models here.

class Customer(models.Model):
    # 地址 
    address = models.CharField(max_length=200)
    # 名字
    name = models.CharField(max_length=200)
    # 电话号码
    phonenumber = models.CharField(max_length=200)
    # 主机名
    idcard = models.CharField(max_length=200)
