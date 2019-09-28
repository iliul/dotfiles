# -*- coding: utf-8 -*-
import datetime
import requests
from requests_toolbelt.utils import dump
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user = 'admin:subuser'
key = 'TJjf3gTwfKTDPljHjHaP7lsxESgEhKv3XAr5tzDn'
host = '10.254.9.20:7480'

#get auth
timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
headers = {'Host': host,'Date': timestr,'X-Auth-User':user,'X-Auth-Key':key}
response = requests.get('http://' + host + '/auth/1.0',headers=headers)

#get obj
timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
headers = {'Host': host,'Date': timestr,'X-Auth-Token':response.headers['X-Auth-Token'],'Range':'bytes=0-25'}
response = requests.get('http://' + host + '/swift/v1/testbucekt/yuliyang.s3cfg',headers=headers)

logger.info("response: \n"+response.content)

# data = dump.dump_all(response)
# print(data.decode('utf-8'))
