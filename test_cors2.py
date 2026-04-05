import urllib.request
from urllib.error import HTTPError

req = urllib.request.Request('http://127.0.0.1:8001/test', method='OPTIONS')
req.add_header('Origin', 'http://localhost:5173')
req.add_header('Access-Control-Request-Method', 'PATCH')

try:
    r = urllib.request.urlopen(req)
    print("Status:", r.status)
    print("Headers:", r.headers)
except HTTPError as e:
    print("Status:", e.code)
    print("Headers:", e.headers)
    print("Body:", e.read())
