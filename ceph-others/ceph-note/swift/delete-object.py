# -*- coding: utf-8 -*-
import hmac
import hashlib
import base64
import datetime
import sys
import requests
from requests_toolbelt.utils import dump

user = 'admin:subuser'
key = 'TJjf3gTwfKTDPljHjHaP7lsxESgEhKv3XAr5tzDn'
host = '10.254.9.20:7480'


#get auth
timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
headers = {'Host': host,'Date': timestr,'X-Auth-User':user,'X-Auth-Key':key}
response = requests.get('http://' + host + '/auth/1.0',headers=headers)

#delete obj
timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
headers = {'Host': host,'Date': timestr,'X-Auth-Token':response.headers['X-Auth-Token']}
response = requests.delete('http://' + host + '/swift/v1/testbucekt/yuliyang.s3cfg',headers=headers)

data = dump.dump_all(response)
print(data.decode('utf-8'))
