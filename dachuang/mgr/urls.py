from django.urls import path

from mgr import customer

urlpatterns = [

    path('customers', customer.dispatcher),
]

# 凡是 API 请求url为 /api/mgr/customers 的，都交由 我们上面定义的dispatch函数进行分派处理