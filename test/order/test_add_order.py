import requests
import json
 
def test():
    url = "http://localhost:8000/api/mgr/orders"    #测试的接口url
    headers = {"Content-Type":"application/json"}   
    payload = {
        "action":"add_order",
        "data":{
            "name":"华山医院订单002",
            "customerid":1,
            "user_request":"这里是客户请求",
            "dealwith":"这里是解决方案",
            "remarks":"这里是备注信息",
            "ipinfoid":"1"
        }
    }
    r = requests.post(url = url,json = payload,headers = headers)    #发送请求
    #return r.json
    print (r.text)                                                #获取响应报文
    print (r.status_code)
    
if __name__=="__main__":
    test()
