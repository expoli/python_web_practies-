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
    # 主机名
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
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

# Order 订单系统
class Order(models.Model):
    # 订单名
    name = models.CharField(max_length=200,null=True,blank=True)

    # 创建日期
    create_date = models.DateTimeField(default=datetime.datetime.now)

    # 客户请求
    request = models.CharField(max_length=6666)

    # 解决方案
    dealwith = models.CharField(max_length=6666)

    # 备注
    remarks = models.CharField(max_length=6666)

    # 客户 禁止删除记录。PROTECT
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

