#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from http import cookiejar
from urllib import error, parse, request

import mysql.connector
import requests


class get_openwrt_status(object):

    def __init__(self):
        self.dhcp_json = {'ipv4': [], 'ipv6': []}
        self.overview_json = {}
        self.login_url = 'http://192.168.178.1/cgi-bin/luci'
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36'}
        self.head = {'User-Agent': r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36', 'Connection': 'keep-alive'}
        self.Login_Data = {'luci_username': 'root',
                           'luci_password': 'Mmhjd4321'}

    def set_login_data(self, luci_username='root', luci_password='Mmhjd4321'):
        self.Login_Data['luci_username'] = luci_username
        self.Login_Data['luci_password'] = luci_password

    def set_login_url(self, login_url='http://192.168.178.1/cgi-bin/luci'):
        self.login_url = login_url

    def get_cookies(self):

        data_url = 'http://192.168.178.1/cgi-bin/luci/admin/status/overview'
        dhcplease_status_url = 'http://192.168.178.1/cgi-bin/luci/admin/network/dhcplease_status?'
        overview_status_url = 'http://192.168.178.1/cgi-bin/luci/admin/status/overview?status=1'
        upnp_status_url = 'http://192.168.178.1/cgi-bin/luci/admin/services/upnp/status?'

        login_post_data = parse.urlencode(self.Login_Data).encode('utf-8')
        #
        cookie = cookiejar.CookieJar()
        #
        cookie_support = request.HTTPCookieProcessor(cookie)
        #
        opener = request.build_opener(cookie_support)
        #
        req1 = request.Request(
            url=self.login_url, data=login_post_data, headers=self.head)
        req2 = request.Request(url=data_url, headers=self.head)
        dhcp_req = request.Request(url=dhcplease_status_url, headers=self.head)
        overview_req = request.Request(
            url=overview_status_url, headers=self.head)

        try:
            response1 = opener.open(req1)
            response2 = opener.open(req2)
            dhcp_response = opener.open(dhcp_req)
            overview_renponse = opener.open(overview_req)

            dhcp_html = dhcp_response.read()
            dhcp_json = json.loads(dhcp_html)
            for i in dhcp_json[0]:
                self.dhcp_json['ipv4'].append(i)
            for i in dhcp_json[1]:
                self.dhcp_json['ipv6'].append(i)

            overview_html = overview_renponse.read()
            overview_json = json.loads(overview_html)
            self.overview_json['wan'] = overview_json.get('wan')
            self.overview_json['wan6'] = overview_json.get('wan6')
        except error.URLError as e:
            if hasattr(e, 'code'):
                print("HTTPError:%d" % e.code)
            elif hasattr(e, 'reason'):
                print("URLError:%s" % e.reason)

    def print_info(self):
        for i in self.dhcp_json:
            print(i)
        print("wan: %s" % self.overview_json.get('wan'))
        print("wan6: %s" % self.overview_json.get('wan6'))
        pass

    def get_dhcp_json(self):
        return self.dhcp_json

    def get_overview_json(self):
        return self.overview_json


class write_ipv4_info(object):
    def __init__(self):
        self.macaddr = []
        self.hostname = []
        self.ipaddr = []
        self.db_table_name = []

    def set_value(self, ipv4_dhcp_json, db_table_name):
        self.macaddr = ipv4_dhcp_json['macaddr']
        self.hostname = ipv4_dhcp_json['hostname']
        self.ipaddr = ipv4_dhcp_json['ipaddr']
        self.db_table_name = db_table_name

    def write_to_db(self):
        # 打开数据库链接
        openwrt_db = mysql.connector.connect(
            host="localhost",
            user='openwrt',
            passwd='openwrt',
            database='openwrt'
        )

        # 使用 cursor（） 获取操作游标
        cursor = openwrt_db.cursor()

        # 如果我们要读取指定条件的数据，可以使用 where 语句：
        sql = "SELECT * FROM "\
            + self.db_table_name\
            + " WHERE 4macaddr = "\
            + "\'"\
            + self.macaddr\
            + "\'"

        val = (self.db_table_name, self.macaddr,)
        #
        cursor.execute(sql)
        myresult = cursor.fetchall()
        if (myresult):
            print("already exited,updating...")
            # 为了防止数据库查询发生 SQL 注入的攻击，我们可以使用 %s 占位符来转义更新语句的条件：
            # sql = "UPDATE openwrt SET ipversion = %s WHERE ipversion = %s"
            sql = "UPDATE " \
                + self.db_table_name \
                + " SET " \
                + "4macaddr" \
                + " = " \
                + "\'"\
                + self.macaddr\
                + "\'"\
                + " WHERE " \
                + "4addr" \
                + " = "\
                + "\'"\
                + self.ipaddr \
                + "\'"
            # sql = "UPDATE %s SET  %s = %s WHERE %s = %s"
            # val = (self.db_table_name,"4macaddr",self.macaddr,"4addr",self.ipaddr)
            cursor.execute(sql)
            openwrt_db.commit()

            sql = "UPDATE " \
                + self.db_table_name \
                + " SET " \
                + "4macaddr" \
                + " = " \
                + "\'"\
                + self.macaddr\
                + "\'"\
                + " WHERE " \
                + "4hostname" \
                + " = "\
                + "\'"\
                + self.hostname \
                + "\'"
            # sql = "UPDATE %s SET  %s = %s WHERE %s = %s"
            # val = (self.db_table_name,"4macaddr",self.macaddr,"4hostname",self.hostname)
            cursor.execute(sql)
            openwrt_db.commit()
            print(cursor.rowcount, " 条记录被修改")
            # 关闭数据库
            openwrt_db.close()
        else:
            # 使用 cursor（） 获取操作游标
            cursor = openwrt_db.cursor()

            # 使用execute方法执行SQL语句
            # 插入数据
            sql = "INSERT INTO ipv4dhcpstatus (4addr, 4hostname,4macaddr,ipversion) VALUES (%s, %s,%s,%s)"
            val = (self.ipaddr, self.hostname, self.macaddr, 4)
            cursor.execute(sql, val)
            openwrt_db.commit()    # 数据表内容有更新，必须使用到该语句
            print(cursor.rowcount, "记录插入成功。")
            # 关闭数据库
            openwrt_db.close()


class write_ipv6_info(object):
    def __init__(self):
        self.ipv6addr = []
        self.ipv6name = []
        self.ipv6uuid = []
        self.db_table_name = []

    def set_value(self, ipv6_dhcp_json, db_table_name):
        self.ipv6addr = ipv6_dhcp_json['macaddr']
        self.ipv6name = ipv6_dhcp_json['hostname']
        self.ipv6uuid = ipv6_dhcp_json['ipaddr']
        self.db_table_name = db_table_name

    def write_to_db(self):
        # 打开数据库链接
        openwrt_db = mysql.connector.connect(
            host="localhost",
            user='openwrt',
            passwd='openwrt',
            database='openwrt'
        )
        # 使用 cursor（） 获取操作游标
        cursor = openwrt_db.cursor()

        # 如果我们要读取指定条件的数据，可以使用 where 语句：
        sql = "SELECT * FROM dhcpstatus WHERE 6uuid = %s"
        val = (self.ipv6uuid,)
        #
        cursor.execute(sql, val)
        myresult = cursor.fetchall()
        if (myresult):
            print("already exited,updating...")
            # 为了防止数据库查询发生 SQL 注入的攻击，我们可以使用 %s 占位符来转义更新语句的条件：
            # sql = "UPDATE openwrt SET ipversion = %s WHERE ipversion = %s"
            sql = "UPDATE " \
                + self.db_table_name \
                + " SET " \
                + "6uuid" \
                + " = " \
                + "\'"\
                + self.ipv6uuid\
                + "\'"\
                + " WHERE " \
                + "6addr" \
                + " = "\
                + "\'"\
                + self.ipv6addr \
                + "\'"
            # sql = "UPDATE %s SET  %s = %s WHERE %s = %s"
            # val = (self.db_table_name,"4macaddr",self.macaddr,"4addr",self.ipaddr)
            cursor.execute(sql)
            openwrt_db.commit()

            sql = "UPDATE " \
                + self.db_table_name \
                + " SET " \
                + "6uuid" \
                + " = " \
                + "\'"\
                + self.ipv6uuid\
                + "\'"\
                + " WHERE " \
                + "6name" \
                + " = "\
                + "\'"\
                + self.ipv6name \
                + "\'"
            # sql = "UPDATE %s SET  %s = %s WHERE %s = %s"
            # val = (self.db_table_name,"4macaddr",self.macaddr,"4hostname",self.hostname)
            cursor.execute(sql)
            openwrt_db.commit()
            print(cursor.rowcount, " 条记录被修改")
            # 关闭数据库
            openwrt_db.close()
        else:
            # 使用 cursor（） 获取操作游标
            cursor = openwrt_db.cursor()

            # 使用execute方法执行SQL语句
            # 插入数据
            sql = "INSERT INTO ipv6dhcpstatus (6addr, 6name,6uuid,ipversion) VALUES (%s, %s,%s,%s)"
            val = (self.ipv6addr, self.ipv6name, self.ipv6uuid, 6)
            cursor.execute(sql, val)
            openwrt_db.commit()    # 数据表内容有更新，必须使用到该语句
            print(cursor.rowcount, "记录插入成功。")
            # 关闭数据库
            openwrt_db.close()


class write_center_info(object):
    def __init__(self):
        self.ipversion = []
        self.usernumber = []
        self.db_table_name = []

    def set_value(self, center_json, db_table_name):
        self.ipversion = center_json['ipversion']
        self.usernumber = center_json['userbunber']
        self.db_table_name = db_table_name

    def write_to_db(self, db_table_name):
        # 打开数据库链接
        openwrt_db = mysql.connector.connect(
            host="localhost",
            user='openwrt',
            passwd='openwrt',
            database='openwrt'
        )
        # 使用 cursor（） 获取操作游标
        cursor = openwrt_db.cursor()

        # 如果我们要读取指定条件的数据，可以使用 where 语句：
        sql = "SELECT * FROM %s WHERE 6uuid = %s"
        val = (self.db_table_name, self.ipversion,)
        #
        cursor.execute(sql, val)
        myresult = cursor.fetchall()
        if (myresult):
            print("already exited,updating...")
            # 为了防止数据库查询发生 SQL 注入的攻击，我们可以使用 %s 占位符来转义更新语句的条件：
            # sql = "UPDATE openwrt SET ipversion = %s WHERE ipversion = %s"
            sql = "UPDATE " \
                + self.db_table_name \
                + " SET " \
                + "ipversion" \
                + " = " \
                + "\'"\
                + self.ipversion\
                + "\'"\
                + " WHERE " \
                + "usernamber" \
                + " = "\
                + "\'"\
                + self.usernumber \
                + "\'"
            # sql = "UPDATE %s SET  %s = %s WHERE %s = %s"
            # val = (self.db_table_name,"4macaddr",self.macaddr,"4addr",self.ipaddr)
            cursor.execute(sql)
            openwrt_db.commit()
            print(cursor.rowcount, " 条记录被修改")
            # 关闭数据库
            openwrt_db.close()
        else:
            # 使用 cursor（） 获取操作游标
            cursor = openwrt_db.cursor()

            # 使用execute方法执行SQL语句
            # 插入数据
            sql = "INSERT INTO %s (ipversion, usernumber) VALUES (%s, %s)"
            val = (self.db_table_name, self.ipversion, self.usernumber,)
            cursor.execute(sql, val)
            openwrt_db.commit()    # 数据表内容有更新，必须使用到该语句
            print(cursor.rowcount, "记录插入成功。")
            # 关闭数据库
            openwrt_db.close()


def test_add_ipinfo(dhcp_json):
    url = "http://yutang.expoli.tech/api/mgr/ipinfos"  # 测试的接口url
    headers = {"Content-Type": "application/json"}
    # 获取ipv4的数量
    number = len(dhcp_json['ipv4'])
    # 遍历 IP 数据
    for i in range(number):
        # 取得 hostname
        hostname = dhcp_json['ipv4'][i]['hostname']
        # 取得 ipv4 地址
        ipv4addr = dhcp_json['ipv4'][i]['ipaddr']
        # 取得 mac 地址
        macaddr = dhcp_json['ipv4'][i]['macaddr']
        # 遍历 ipv6 数据查看主机是否有ipv6地址
        for j in dhcp_json['ipv6']:
            # 如果已有此计算机
            if j['hostname'] == hostname:
                # 取得 ipv6 地址
                ipv6addr = j['ip6addr']
                # 取得 duid
                duid = j['duid']
                # 防止复写
                break
            else:
                # 没有地址，置为null
                ipv6addr = 'null'
                duid = 'null'
        # 查询 api 参数
        list_payload = {
            "action": "list_ipinfo",
            "pagenum": 1,
            "pagesize": 8,
            'keywords': hostname
        }
        r = requests.post(url=url, json=list_payload, headers=headers)  # 发送请求
        # 将结果转化为字符串
        tmp = r.text
        # 将字符串 转化为 json
        list_json = json.loads(tmp)
        total_num = list_json['total']

        if total_num:
            id = list_json['retlist'][0]['id']
            update_payload = {
                "action": "modify_ipinfo",
                "id": id,
                "newdata": {
                    "hostname": hostname,
                    "ipv4addr": ipv4addr,
                    "macaddr": macaddr,
                    "ipv6addr": ipv6addr,
                    "duid": duid
                }
            }
            r = requests.post(url=url, json=update_payload,
                              headers=headers)  # 发送请求
            # return r.json
            print(r.text)  # 获取响应报文
            print(r.status_code)
            pass
        else:
            # 添加数据的post请求包
            payload = {
                "action": "add_ipinfo",
                "data": {
                    "hostname": hostname,
                    "ipv4addr": ipv4addr,
                    "macaddr": macaddr,
                    "ipv6addr": ipv6addr,
                    "duid": duid
                }
            }
            r = requests.post(url=url, json=payload, headers=headers)  # 发送请求
            # return r.json
            print(r.text)  # 获取响应报文
            print(r.status_code)


if __name__ == "__main__":

    openwrt_status = get_openwrt_status()
    print('请输入登录地址；默认地址为http://192.168.178.1/cgi-bin/luci')
    openwrt_status.set_login_url()
    openwrt_status.set_login_data()
    openwrt_status.get_cookies()
    openwrt_status.print_info()

    dhcp_json = openwrt_status.get_dhcp_json()
    test_add_ipinfo(dhcp_json)
    overview_json = openwrt_status.get_overview_json()
