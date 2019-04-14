import json

from django.http import JsonResponse

# 导入 IPinfo 对象定义
from common.models import IPinfo

import traceback
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q


def listipinfo(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = IPinfo.objects.values().order_by('-id')

        # 查看是否有 关键字 搜索 参数
        keywords = request.params.get('keywords',None)
        if keywords:
            conditions = [Q(name__contains=one) for one in keywords.split(' ') if one]
            query = Q()
            for condition in conditions:
                query &= condition
            qs = qs.filter(query)
        
        # 要获取的第几页
        pagenum = request.params['pagenum']

        # 每页要显示多少条记录
        pagesize = request.params['pagesize']

        # 使用分页对象，设定每页多少条记录
        pgnt = Paginator(qs, pagesize)

        # 从数据库中读取数据，指定读取其中第几页
        page = pgnt.page(pagenum)

        # 将 QuerySet 对象 转化为 list 类型
        retlist = list(page)

        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist,'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2,  'msg': f'未知错误\n{traceback.format_exc()}'})


def addipinfo(request):

    info = request.params['data']

    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    ipinfo = IPinfo.objects.create(hostname=info['hostname'],
                                   ipv4addr=info['ipv4addr'],
                                   macaddr=info['macaddr'],
                                   ipv6addr=info['ipv6addr'],
                                   duid=info['duid']
                                #    customer_id=info['customerid']
                                   )

    return JsonResponse({'ret': 0, 'id': ipinfo.id})


def modifyipinfo(request):

    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作

    ipinfoid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        ipinfo = IPinfo.objects.get(id=ipinfoid)
    except ipinfo.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{ipinfoid}`的药品不存在'
        }

    if 'hostname' in newdata:
        ipinfo.hostname = newdata['hostname']
    if 'ipv4addr' in newdata:
        ipinfo.ipv4addr = newdata['ipv4addr']
    if 'macaddr' in newdata:
        ipinfo.macaddr = newdata['macaddr']
    if 'ipv6addr' in newdata:
        ipinfo.ipv6addr = newdata['ipv6addr']
    if 'duid' in newdata:
        ipinfo.duid = newdata['duid']
    # if 'customer_id' in newdata:
    #     ipinfo.customer_id = newdata['customer_id']

    # 注意，一定要执行save才能将修改信息保存到数据库
    ipinfo.save()

    return JsonResponse({'ret': 0})


def deleteipinfo(request):

    ipinfoid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的IP记录
        ipinfo = IPinfo.objects.get(id=ipinfoid)
    except ipinfo.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{ipinfoid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    ipinfo.delete()

    return JsonResponse({'ret': 0})

from lib.handler import dispatcherBase

Action2Handler = {
    'list_ipinfo': listipinfo,
    'add_ipinfo': addipinfo,
    'modify_ipinfo': modifyipinfo,
    'del_ipinfo': deleteipinfo,
}


def dispatcher(request):
    return dispatcherBase(request, Action2Handler)
