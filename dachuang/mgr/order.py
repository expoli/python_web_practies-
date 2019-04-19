import json,traceback

from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse

# 导入 Order 对象定义
from common.models import Order, OrderIPinfo

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q


def addorder(request):

    info = request.params['data']

    # 从请求消息中 获取要添加订单的信息
    # 并且插入到数据库中

    # with transaction.atomic() 下面 缩进部分的代码，
    # 对数据库的操作，就都是在 一个事务 中进行了。
    # 如果其中有任何一步数据操作失败了， 前面的操作都会回滚。
    with transaction.atomic():
        new_order = Order.objects.create(name=info['name'],
                                         customer_id=info['customerid'],
                                         user_request=info['user_request'],
                                         dealwith=info['dealwith'],
                                         remarks=info['remarks']
                                         )

        batch = [OrderIPinfo(order_id=new_order.id, ipinfo_id=info['ipinfoid'])]
        OrderIPinfo.objects.bulk_create(batch)
    # 使用 bulk_create， 参数是一个包含所有 该表的 Model 对象的 列表

    return JsonResponse({'ret': 0, 'id': new_order.id})

# 取 外键关联的表记录的字段值，在Django中很简单，可以直接通过
# 外键字段 后面加 两个下划线 加 关联字段名的方式 来获取。


def listorder(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = Order.objects\
            .annotate(
                customer_name=F('customer__name'),
                ipinfos_hostname=F('ipinfo__hostname')
            )\
            .values(
                'id', 'name', 'create_date', 'user_request', 'dealwith', 'remarks', 'customer_name', 'ipinfos_hostname'
            ).order_by('-id')

        # 查看是否有 关键字 搜索 参数
        keywords = request.params.get('keywords',None)
        if keywords:
            # hostname__contains 为数据表键值
            conditions = [Q(hostname__contains=one) for one in keywords.split(' ') if one]
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

def deleteorder(request):
    # 获取订单ID
    oid = request.params['id']

    try:

        one = Order.objects.get(id=oid)
        with transaction.atomic():

            # 一定要先删除 OrderIPinfo 里面的记录
            OrderIPinfo.objects.filter(order_id=oid).delete()
            # 再删除订单记录
            one.delete()

        return JsonResponse({'ret': 0, 'id': oid})

    except Order.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': f'id 为`{oid}`的订单不存在'
        })

    except:
        err = traceback.format_exc()
        return JsonResponse({'ret': 1, 'msg': err})


from lib.handler import dispatcherBase

Action2Handler = {
    'list_order': listorder,
    'add_order': addorder,
    'delete_order': deleteorder,
}


def dispatcher(request):
    return dispatcherBase(request, Action2Handler)
