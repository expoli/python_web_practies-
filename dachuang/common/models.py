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
    hostname = models.CharField(max_length=200)
    # ipv4地址
    ipv4addr = models.CharField(max_length=200)
    # mac 地址
    macaddr = models.CharField(max_length=200)
    # ipv6地址
    ipv6addr = models.CharField(max_length=200)
    # duid
    duid = models.CharField(max_length=200)
