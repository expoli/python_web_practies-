import requests
import json
 
def test():
    url = "http://yutang.expoli.tech/api/mgr/ipinfos"    #测试的接口url
    headers = {"Content-Type":"application/json"}   
    payload = {
        "action":"add_ipinfo",
        "data":{
            "hostname": "DESKTOP-CAKF83U", 
            "ipv4addr": "192.168.0.78", 
            "macaddr": "34:97:F6:E0:1D:E2", 
            "ipv6addr": "2001:da8:5000:5020:f5bb:a892:6a9:d7ef", 
            "duid" : "adadasasdasfdfa",
            "customerid": "1"
        }
    }
    r = requests.post(url = url,json = payload,headers = headers)    #发送请求
    #return r.json
    print (r.text)                                                #获取响应报文
    print (r.status_code)
    
if __name__=="__main__":
    test()
