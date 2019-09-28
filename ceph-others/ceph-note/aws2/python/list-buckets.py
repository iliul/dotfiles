# -*- coding: utf-8 -*-
import hmac
import hashlib
import base64 
import datetime
import sys
import requests
from requests_toolbelt.utils import dump

if len(sys.argv) < 3:
    print('bad syntax, usage: {script_name} host bname')
    exit()
host, bname = sys.argv[1], sys.argv[2]
access_key = 'admin'
secret_key = 'admin'
timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
hstr = ''
hstr += 'GET\n'
hstr += '\n'
hstr += '\n'
hstr += timestr + '\n'
hstr += '/' + bname
key = bytearray(secret_key, 'utf-8')
hres = hmac.new(key, hstr.encode('utf-8'), hashlib.sha1).digest()
hres = base64.b64encode(hres)
hres = hres.decode('utf-8')
headers = {'Host': host,'Date': timestr,'Authorization':'AWS ' + access_key + ':' + hres}
response = requests.get('http://' + host + '/' + bname,headers=headers)

data = dump.dump_all(response)
print(data.decode('utf-8'))

