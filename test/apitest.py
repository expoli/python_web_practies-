import  requests,pprint

class APITEST(object):

    def __init__(self):
        self.server_url = 'http://localhost:8000'

    def test_login_in_out(self):
        api_value = '/api/mgr/signin'
        payload = {
            'username': 'byhy',
            'password': '88888888'
        }
        url = self.server_url+api_value
        response = requests.post(url,data=payload)

        pprint.pprint(response.json())

    def test_get_customers_info(self):
        api_value = '/api/mgr/customers'
        payload = {
            "action": "list_customer",
            "pagesize": 2
        }
        url = self.server_url+api_value
        response = requests.get(url,payload)

        pprint.pprint(response.json)

    def test_add_one_customer(self):
        api_value = '/api/mgr/customers'
        payload = {
            "action":"add_customer",
            "data":{
                "address": "江苏省常州武进市白云街44号",
                "name": "武进市 袁腾飞",
                "phonenumber": "13886666666",
                "idcard": "aaaaaaaaaaaaaaaa"
            }
        }
        url = self.server_url+api_value
        response = requests.post(url,data=payload)

        pprint.pprint(response.json())
    
    def test_update_customer(self):
        api_value = '/api/mgr/customers'
        payload = {
            "action":"modify_customer",
            "id": 6,
            "newdata":{
                "address": "江苏省常州武进市白云街44号",
                "name": "武进市 袁腾飞",
                "phonenumber": "13886666666",
                "idcard": "aaaaaaaaaaaaaaaa"
            }
        }
        url = self.server_url+api_value
        response = requests.put(url,data=payload)

        pprint.pprint(response.json())

    def test_del_customer(self):
        api_value = '/api/mgr/customers'
        payload = {
            "action":"del_customer",
            "id": 6
        }
        url = self.server_url+api_value
        response = requests.delete(url,data=payload)

        pprint.pprint(response.json())

    def test_list_ipinfo(self):
        api_value = '/api/mgr/ipinfo'
        url = self.server_url+api_value
        response = requests.get(url)

        pprint.pprint(response.json())

    def test_add_ipinfo(self):
        api_value = '/api/mgr/ipinfo'
        payload = {
            "action":"add_ipinfo",
            "data":{
                "hostname": "DESKTOP-CAKF83U", 
                "ipv4addr": "192.168.0.78", 
                "macaddr": "34:97:F6:E0:1D:E2", 
                "ipv6addr": "2001:da8:5000:5020:f5bb:a892:6a9:d7ef", 
                "duid" : "adadasasdasfdfa"
            }
        }
        url = self.server_url+api_value
        response = requests.post(url,data=payload)

        pprint.pprint(response.json())

    def test_update_ipinfo(self):
        api_value = '/api/mgr/ipinfo'
        payload = {
            "action":"modify_ipinfo",
            "id": 6,
            "newdata":{
                "hostname": "DESKTOP-CAKF83U", 
                "ipv4addr": "192.168.0.78", 
                "macaddr": "34:97:F6:E0:1D:E2", 
                "ipv6addr": "2001:da8:5000:5020:f5bb:a892:6a9:d7ef", 
                "duid" : "adadasasdasfdfa"
            }
        }
        url = self.server_url+api_value
        response = requests.put(url,data=payload)

        pprint.pprint(response.json())
    
    def test_del_ipinfo(self):
        api_value = '/api/mgr/ipinfo'
        payload = {
            "action":"del_ipinfo",
            "id": 6
        }
        url = self.server_url+api_value
        response = requests.delete(url,data=payload)

        pprint.pprint(response.json())

    def test_list_orders(self):
        api_value = '/api/mgr/orders'
        # payload = 
        url = self.server_url+api_value
        response = requests.post(url)

        pprint.pprint(response.json())

    def test_add_order(self):
        api_value = '/api/mgr/orders'
        payload = {
            "action":"add_order",
            "data":{
                "name":"华山医院订单002",
                "customerid":3,
                "ipinfolist":[
                    {"id":16,"request":"这里是客户请求","dealwith":"这里是解决方案","remarks":"这里是备注信息"},
                    {"id":15,"request":"这里是客户请求","dealwith":"这里是解决方案","remarks":"这里是备注信息"}
                ]
            }
        }
        url = self.server_url+api_value
        response = requests.post(url,data=payload)

        pprint.pprint(response.json())
    
    def test_del_order(self):
        api_value = '/api/mgr/orders'
        payload = {
            "action":"delete_order",
            "id": 6
        }
        url = self.server_url+api_value
        response = requests.delete(url,data=payload)

        pprint.pprint(response.json())

if __name__ == "__main__":
    apitest = APITEST()
    apitest.test_login_in_out()
    apitest.test_add_one_customer()
    apitest.test_get_customers_info()
    apitest.test_update_customer()
    apitest.test_del_customer()
    apitest.test_list_ipinfo()


#http://localhost:8000/api/mgr/customers?action=list_customer&_=1555149721722