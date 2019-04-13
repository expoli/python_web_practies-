import json

from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse

# 导入 Order 对象定义
from common.models import Order, OrderIPinfo


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

        batch = [OrderIPinfo(order_id=new_order.id, ipinfo_id=mid)
                 for mid in info['ipinfoid']]
        OrderIPinfo.objects.bulk_create(batch)
    # 使用 bulk_create， 参数是一个包含所有 该表的 Model 对象的 列表

    return JsonResponse({'ret': 0, 'id': new_order.id})

# 取 外键关联的表记录的字段值，在Django中很简单，可以直接通过
# 外键字段 后面加 两个下划线 加 关联字段名的方式 来获取。


def listorder(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Order.objects\
        .annotate(
            customer_name=F('customer__name'),
            ipinfos_hostname=F('ipinfos__hostname')
        )\
        .values(
            'id', 'name', 'create_date', 'user_request', 'dealwith', 'remarks'
        )

    # 将 QuerySet 对象 转化为 list 类型
    retlist = list(qs)

    # 可能有 ID相同，药品不同的订单记录， 需要合并
    newlist = []
    id2order = {}
    for one in retlist:
        orderid = one['id']
        if orderid not in id2order:
            newlist.append(one)
            id2order[orderid] = one
        else:
            id2order[orderid]['medicines_name'] += ' | ' + \
                one['medicines_name']

    return JsonResponse({'ret': 0, 'retlist': newlist})

from lib.handler import dispatcherBase

Action2Handler = {
    'list_order': listorder,
    'add_order': addorder,
}


def dispatcher(request):
    return dispatcherBase(request, Action2Handler)
