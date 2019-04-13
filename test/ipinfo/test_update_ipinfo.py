import requests
import json
 
def test():
    url = "http://localhost:8000/api/mgr/ipinfos"    #测试的接口url
    headers = {"Content-Type":"application/json"}   
    payload = {
        "action":"modify_ipinfo",
        "id": 1,
        "newdata":{
            "hostname": "test", 
            "ipv4addr": "192.168.0.99", 
            "macaddr": "34:97:F6:E0:1D:E8", 
            "ipv6addr": "2001:da8:5000:5020:f5bb:a892:6a9:d7ef", 
            "duid": "aaaaaaaa",
            "customerid": "2"
        }
    }
    r = requests.put(url = url,json = payload,headers = headers)    #发送请求
    #return r.json
    print (r.text)                                                #获取响应报文
    print (r.status_code)
    
if __name__=="__main__":
    test()
