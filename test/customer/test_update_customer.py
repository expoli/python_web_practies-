import requests
import json
 
def test():
    url = "http://localhost:8000/api/mgr/customers"    #测试的接口url
    headers = {"Content-Type":"application/json"}   
    payload = {
        "action":"modify_customer",
        "id": 1,
        "newdata":{
            "address": "江苏省常州武进市白云街44号",
            "name": "武进市 袁腾飞",
            "phonenumber": "13886666666",
            "idcard": "bbbbbbbbb"
        }
    }
    r = requests.post(url = url,json = payload,headers = headers)    #发送请求
    #return r.json
    print (r.text)                                                #获取响应报文
    print (r.status_code)
    
if __name__=="__main__":
    test()
