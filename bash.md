# 启动 django 进程

python3 manage.py runserver 0.0.0.0:8000 &

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

