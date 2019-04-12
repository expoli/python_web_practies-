from django.shortcuts import render
## 
from django.http import HttpResponse

# Create your views here.

# 先定义好HTML模板
html_template ='''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
table {
    border-collapse: collapse;
}
th, td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
</style>
</head>
    <body>
        <table>
        <tr>
        <th>id</th>
        <th>IP协议版本</th>
        <th>用户数量</th>
        </tr>
        

        {% for ipv in ipversion %}
            <tr>
            <!-- name与value只是两个字典变量代号 -->
            {% for name, value in ipv.items %}
                <td>{{ value }}</td>            
            {% endfor %}
            </tr>
        {% endfor %}

        
                
        </table>
    </body>
</html>
'''
from django.template import engines
django_engine = engines['django']
template = django_engine.from_string(html_template)


# 导入 common center 对象

from common.models import Customer

def list_all_user_info(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    qs = Customer.objects.values()

    # 检查url中是否有参数ipversion
    # 第二个参数传入 None 表示，如果没有 phonenumber 参数在 querystring中 ，就会返回 None
    ipv =  request.GET.get('name',None)

    # 如果有，添加过滤条件
    # 然后通过调用 QuerySet 对象的filter方法，就可以把查询过滤条件加上去
    # 有了这个过滤条件，Django 会在底层执行数据库查询的SQL语句 加上相应的 where 从句，进行过滤查询。
    # 注意，参数名 phonenumber 是和 定义的表 model 的属性名 phonenumber 一致的。
    # filter的过滤条件可以有多个，只要继续在后面的参数添加过滤条件即可。
    # http://localhost:8000/manager/users/?ipversion=ipv4
    if ipv:
        qs = qs.filter(name=ipv)


    # 传入渲染模板需要的参数
    rendered = template.render({'name':qs})

    return HttpResponse(rendered)