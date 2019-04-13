import requests
import json
 
def test():
    url = "http://localhost:8000/api/mgr/customers"    #测试的接口url
    headers = {"Content-Type":"application/json"}   
    payload = {
        "action":"add_customer",
        "data":{
            "address": "河南省郑州市武100号",
            "name": "超哥哥",
            "phonenumber": "1388888888",
            "idcard": "***************"
        }
    }
    r = requests.post(url = url,json = payload,headers = headers)    #发送请求
    #return r.json
    print (r.text)                                                #获取响应报文
    print (r.status_code)
    
if __name__=="__main__":
    test()
