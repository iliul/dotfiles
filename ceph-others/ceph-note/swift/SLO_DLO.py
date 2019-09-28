# -*- coding: utf-8 -*-

import swiftclient
import swiftclient.service
from swiftclient.service import SwiftService
import time
import json

swift_conn = swiftclient.Connection(
    user="cinder-yuliyang:swift",
    key="E7e78CE672jB5t5KFgtcPGIQ1Vrakdp0OtPyNeSO",
    tenant_name="cinder-yuliyang",
    authurl="http://10.142.50.24:8082/auth",
    auth_version="1",
)

swift_options = {
    "auth_version": "1.0",
    "key": "E7e78CE672jB5t5KFgtcPGIQ1Vrakdp0OtPyNeSO",
    "user": "cinder-yuliyang:swift",
    "auth": "http://10.142.50.24:8082/auth",
}

# Parameters for this run:
containerName = 'bucket2'
fileName = '1GB'
segmentSize = '52428800' #50MiB
fileSize = '1GB'
# Check to see what is available right now:
# swiftclient.service methods
# swiftclient.client methods
myinfo = swift_conn.get_account()
print json.dumps(myinfo, indent=4)
############################################################################
# Check to see what is available right now:
# swiftclient.service methods not used for this, only swiftclient.client
############################################################################
# swiftclient.client methods
# myinfo = swift_conn.get_account()
# print json.dumps(myinfo,indent=4)
# Look into a container
swift_conn.put_container(containerName + '_dlo')
swift_conn.put_container(containerName + '_dlo' + '_segments')
swift_conn.put_container(containerName + '_slo')
swift_conn.put_container(containerName + '_slo' + '_segments')
cont = swift_conn.get_container(containerName + '_dlo' + '_segments')


swift_options = {
    "auth_version": "1.0",
    "key": "E7e78CE672jB5t5KFgtcPGIQ1Vrakdp0OtPyNeSO",
    "user": "cinder-yuliyang:swift",
    "auth": "http://10.142.50.24:8082/auth",
    'segment_size': segmentSize,
}
print ">>>>>>>>>>>>>>>>>>>>>>>>  START DLO"
with SwiftService(swift_options) as sw:
    start_time = time.clock()
    for r in sw.upload(container=containerName + "_dlo",
                       objects=[fileName]):
        print r['success']
        final_time_upload_dlo = (time.clock() - start_time)
############################################################################
# Static Large Objects (SLO) UPLOAD
############################################################################
# Start with a small file: 1.25MB, segment size ~1MB
# upload test


swift_options = {
    "auth_version": "1.0",
    "key": "E7e78CE672jB5t5KFgtcPGIQ1Vrakdp0OtPyNeSO",
    "user": "cinder-yuliyang:swift",
    "auth": "http://10.142.50.24:8082/auth",
    'segment_size': segmentSize,
    'use_slo': True
}
print ">>>>>>>>>>>>>>>>>>>>>>>>  START SLO"
with SwiftService(swift_options) as sw:
    start_time = time.clock()
    for r in sw.upload(container=containerName + "_slo",
                       objects=[fileName]):
        print r['success']
        final_time_upload_slo = (time.clock() - start_time)
############################################################################
# Dynamic Large Objects (DLO) Download
############################################################################
# retreive an object

print ">>>>>>>>>>>>>>>>>>>>>>>> DOWNLOAD DLO"
start_time = time.clock()
obj_tuple = swift_conn.get_object(containerName + "_dlo", fileName)
with open(fileName + 'dlo', 'wb') as my_hello:
    my_hello.write(obj_tuple[1])
    final_time_download_dlo = (time.clock() - start_time)
############################################################################
# Dynamic Large Objects (SLO) Download
############################################################################
# retreive an object

print ">>>>>>>>>>>>>>>>>>>>>>>> DOWNLOAD SLO"
start_time = time.clock()
obj_tuple = swift_conn.get_object(containerName + "_slo", fileName)
with open(fileName + 'slo', 'wb') as my_hello:
    my_hello.write(obj_tuple[1])
    final_time_download_slo = (time.clock() - start_time)
############################################################################
# RESULTS
############################################################################
print ">>>>>>>>>>>>>>>>>>>>>>>> RESULT"
with open('results' + fileSize + segmentSize + '.txt', 'wb') as out:
    out.write('File Size= ' + fileSize + '\n' +
              'Segment Size = ' + segmentSize + '\n' +
              '*************************************\n' +
              'DLO Upload Time: ' + repr(final_time_upload_dlo) + '\n' +
              'SLO Upload Time: ' + repr(final_time_upload_slo) + '\n' +
              'DLO Download Time: ' + repr(final_time_download_dlo) + '\n' +
              'SLO Download Time: ' + repr(final_time_download_slo) + '\n')


############################################################################
# Clean UP
############################################################################
def delContainer(container__name):
    cont = swift_conn.get_container(container__name)
    for obj in range(len(cont[1])):
        swift_conn.delete_object(container__name, cont[1][obj]["name"])
    swift_conn.delete_container(container__name)

#
# delContainer(containerName + "_dlo")
# delContainer(containerName + "_dlo" + '_segments')
# delContainer(containerName + "_slo")
# delContainer(containerName + "_slo" + '_segments')

swift_conn.close()
