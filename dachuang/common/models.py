from django.db import models

# Create your models here.

class center(models.Model):
    # tCP/IP 版本
    ipversion = models.CharField(max_length=128)
    # 用户人数
    usernumber = models.CharField(max_length=255)
