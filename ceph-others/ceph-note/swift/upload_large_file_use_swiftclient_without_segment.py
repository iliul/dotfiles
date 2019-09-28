# -*- coding: utf-8 -*-
#prepare data dd if=/dev/urandom of=4096MB bs=4M count=1024
import swiftclient.service
import sys,os,six
swift_options = {
    "auth_version": "1.0",
    "key": "E7e78CE672jB5t5KFgtcPGIQ1Vrakdp0OtPyNeSO",
    "user": "cinder-yuliyang:swift",
    "auth": "http://10.142.50.24:8082/auth",
}

swift_conn = swiftclient.Connection(
    user=swift_options['user'],
    key=swift_options['key'],
    authurl=swift_options['auth'],
    auth_version=swift_options['auth_version'],
)

import time
print ">>>>>>>>>>>>>>>>>>>>>>load data"
data = open("/root/DATA/4096MB",'r').read()
reader = six.BytesIO(data)
print ">>>>>>>>>>>>>>>>>>>>>>start upload"
start_time = time.time()
swift_conn.put_object("test222","4096MB",contents=reader,content_length=len(data))
spend = (time.time() - start_time)
print ">>>>>>>>>>>>>>>>>>>>>>upload finish"
print spend,"seconds cost"
