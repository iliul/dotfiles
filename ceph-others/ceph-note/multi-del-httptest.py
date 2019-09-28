# -*- coding: utf-8 -*-
import requests
import urllib
import sys
import logging
from requests_toolbelt.utils import dump
from awsauth import S3Auth
host = 'yuliyangdebugweb002.tunnel.qydev.com'
#host = '192.168.10.20:7480'
access_key = 'admin'
secret_key = 'admin'
cmd = '/deletemulti/?delete'
#cmd = urllib.quote(cmd.decode(sys.stdin.encoding).encode('utf8'))
serverurl = 'http://%s' % host
url = 'http://%s%s' % (host,cmd)

content = '''<Delete>
<Object>
<Key>1K</Key>
</Object>
<Object>
<Key>1K-2</Key>
</Object>
<Object>
<Key>21M</Key>
</Object>
<Object>
<Key>4K</Key>
</Object>
<Object>
<Key>4K-2</Key>
</Object>
<Object>
<Key>8K-2</Key>
</Object>
<Object>
<Key>8K</Key>
</Object>
<Object>
<Key>aclobj</Key>
</Object>
<Object>
<Key>version</Key>
</Object>
</Delete>
'''

response = requests.post(url,data=content,auth=S3Auth(access_key, secret_key, serverurl))
data = dump.dump_all(response)
print(data.decode('utf-8'))
