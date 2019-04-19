import requests
import json
import random

def random_name():
    random_name = str(random.randint(0,100)) + "号超哥哥"
    return random_name

def random_phonenumber():
    random_phonenumber = random.randint(10000000000,19999999999)
    return random_phonenumber

def random_idcard():
    random_idcard = random.randint(100000000000000000,999999999999999999)
    return random_idcard

def random_addr():
    random_addr = "河南省郑州市" + str(random.randint(0,100)) + "路" + str(random.randint(0,100)) + "号"
    return random_addr

def test():
    rand_name = random_name()
    rand_phonenumber = random_phonenumber()
    rand_idcard = random_idcard()
    rand_addr = random_addr()

    url = "http://yutang.expoli.tech/api/mgr/customers"    #测试的接口url
    headers = {"Content-Type":"application/json"}   
    payload = {
        "action":"add_customer",
        "data":{
            "address": rand_addr,
            "name": rand_name,
            "phonenumber": rand_phonenumber,
            "idcard": rand_idcard
        }
    }
    r = requests.post(url = url,json = payload,headers = headers)    #发送请求
    #return r.json
    print (r.text)                                                #获取响应报文
    print (r.status_code)
    
if __name__=="__main__":
    for i in range(6):
        test()
