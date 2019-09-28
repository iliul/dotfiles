import requests
import logging
from datetime import *
from requests_toolbelt.utils import dump
from awsauth import S3Auth
# host = 'yuliyangdebugwebjewel.tunnel.qydev.com'
host = 'yuliyangdebugweb68.tunnel.qydev.com'
host = '10.254.9.20:7480'
host = '127.0.0.1:7480'
logging.basicConfig(level=logging.DEBUG)
access_key = 'date2'
secret_key = 'date2'

#cmd = '/1034CST'
cmd = '/%sCST' % (str(datetime.now().date())+"."+str(datetime.now().time()).replace(':','-').replace('.','-'),)
url = 'http://%s%s' % (host,cmd)
response = requests.put(url,auth=S3Auth(access_key, secret_key,service_url=host))

data = dump.dump_all(response)
print(data.decode('utf-8'))
