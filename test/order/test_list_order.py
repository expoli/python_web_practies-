import requests
import json
 
def test():
    url = "http://yutang.expoli.tech/api/mgr/orders"    #测试的接口url
    headers = {"Content-Type":"application/json"}   
    payload = {
        "action":"list_order",
        "pagenum": "1",
        "pagesize": "5"
        }
    r = requests.post(url = url,json = payload,headers = headers)    #发送请求
    #return r.json
    print (r.text)                                                #获取响应报文
    print (r.status_code)
    
if __name__=="__main__":
    test()
