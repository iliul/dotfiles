# -*- coding: utf-8 -*-
import requests
import urllib
import sys
import logging
from requests_toolbelt.utils import dump
from awsauth import S3Auth
host = '192.168.10.20:7480'
access_key = 'admin'
secret_key = 'admin'
cmd = '/acltest/中文'
cmd = urllib.quote(cmd.decode(sys.stdin.encoding).encode('utf8'))
serverurl = 'http://%s' % host
url = 'http://%s%s' % (host,cmd)
content = None
with open('1.txt', 'rb') as fin:
    content = fin.read()
response = requests.put(url,data=content,auth=S3Auth(access_key, secret_key, serverurl))
data = dump.dump_all(response)
print(data.decode('utf-8'))
