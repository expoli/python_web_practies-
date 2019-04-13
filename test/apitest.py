import  requests,pprint

payload = {
    'username': 'byhy',
    'password': '88888888'
}

response = requests.post('http://localhost:8000/api/mgr/signin',
              data=payload)

pprint.pprint(response.json())
