from django.shortcuts import render
## 
from django.http import HttpResponse

# Create your views here.

def all_user_info(request):
    return HttpResponse("下面是系统中所有的用户信息。。。")

# 导入 common center 对象

from common.models import center

def list_all_user_info(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值

    qs = center.objects.values()

    # 检查url中是否有参数phonenumber
    ph =  request.GET.get('phonenumber',None)

    # 如果有，添加过滤条件
    if ph:
        qs = qs.filter(phonenumber=ph)


    # 定义返回字符串
    retStr = ''
    for customer in  qs:
        for ipversion,usernumber in customer.items():
            retStr += f'{ipversion} : {usernumber} | '

        # <br> 表示换行
        retStr += '<br>'

    return HttpResponse(retStr)