import requests
import logging
from requests_toolbelt.utils import dump
from awsauth import S3Auth
host = '192.168.10.20:7480'
access_key = 'admin'
secret_key = 'admin'
cmd = ''
serverurl = 'http://%s' % host
url = 'http://%s%s' % (host,cmd)
response = requests.get(url,auth=S3Auth(access_key, secret_key, serverurl))
data = dump.dump_all(response)
print(data.decode('utf-8'))
