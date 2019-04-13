from django.db import models

# Create your models here.
# 订单系统
import datetime

class Customer(models.Model):
    # 地址 
    address = models.CharField(max_length=200)
    # 名字
    name = models.CharField(max_length=200)
    # 电话号码
    phonenumber = models.CharField(max_length=200)
    # 身份信息
    idcard = models.CharField(max_length=200)

# IPinfo IP 信息

class IPinfo(models.Model):
    # 主机名
    hostname = models.CharField(max_length=200)
    # ipv4 地址
    ipv4addr = models.CharField(max_length=200)
    # mac 地址
    macaddr = models.CharField(max_length=200)
    # ipv6 地址
    ipv6addr = models.CharField(max_length=200)
    # duid
    duid = models.CharField(max_length=200)
    # 客户 删除主键记录和 相应的外键表记录 CASCADE
    # Django发现这样一对一定定义，它会在migrate的时候，
    # 在数据库中定义该字段为外键的同时， 加上 unique=True 约束，
    # 表示在此表中，所有记录的该字段 取值必须唯一，不能重复。
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE)

# Order 订单系统
class Order(models.Model):
    # 订单名
    name = models.CharField(max_length=200,null=True,blank=True)

    # 创建日期
    create_date = models.DateTimeField(default=datetime.datetime.now)

    # 客户请求
    request = models.TextField(max_length=6000)

    # 解决方案
    dealwith = models.TextField(max_length=6000)

    # 备注
    remarks = models.TextField(max_length=6000)

    # 客户 禁止删除记录。PROTECT
    ipinfos = models.ManyToManyField(IPinfo,through='OrderIPinfo')

class OrderIPinfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    ipinfo = models.ForeignKey(IPinfo, on_delete=models.PROTECT)
