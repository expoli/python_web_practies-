from django.urls import path
from mgr import sign_in_out

urlpatterns = [

    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),

]

# 如果有HTTP请求 url是 /api/mgr/signin 就由 sign_in_out.py 里面的signin 函数处理，

# 如果有HTTP请求 url是 /api/mgr/signout 就由 sign_in_out.py 里面的signout 函数处理。
# 凡是 API 请求url为 /api/mgr/customers 的，都交由 我们上面定义的dispatch函数进行分派处理