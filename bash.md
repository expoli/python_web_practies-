# 启动 django 进程

python3 manage.py runserver 0.0.0.0:8000 &
python3 manage.py runserver 0.0.0.0:8000 --insecure

# 创建项目app

python3 manage.py startapp sales 

# 数据库
## 首先我们需要创建数据库，执行如下命令

python3 manage.py migrate

## 定义我们的 数据库表

python3 manage.py startapp common 

## 告诉Django ， 去看看common这个app里面的models.py ，我们已经修改了数据定义， 你现在去产生相应的更新脚本

python3 manage.py makemigrations common

## 数据库创建表

python3 manage.py migrate

## Django Admin 管理数据

python3 manage.py createsuperuser

# 读取数据库数据
## 获取全部记录
```bash
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    qs = Customer.objects.values()
    # 定义返回字符串
    retStr = ''
    for customer in  qs:
        for name,value in customer.items():
            retStr += f'{name} : {value} | '

        # <br> 表示换行
        retStr += '<br>'

    return HttpResponse(retStr)
```

# 代码直接生成HTML

# API

# 创建 mgr应用目录

python3 manage.py startapp mgr 

## 添加处理请求模块 和 url 路由

# 临时取消 CSRF 校验

注意，缺省创建的项目， Django 会启用一个 CSRF （跨站请求伪造） 安全防护机制。
在这种情况下， 所有的Post、PUT 类型的 请求都必须在HTTP请求头中携带用于校验的数据。
为了简单起见，我们先临时取消掉CSRF的 校验机制，等以后有需要再打开。

注释
```bash
# django.middleware.csrf.CsrfViewMiddleware
```