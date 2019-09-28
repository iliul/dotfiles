import boto
import boto.s3.connection
import os
import math
from boto.s3.key import Key
import logging
boto.set_stream_logger('boto')
host = '10.254.3.68'
access_key = 'admin'
secret_key = 'admin'
conn = boto.connect_s3(
                access_key,
                secret_key,
                host = host,
                is_secure = False,
                port = 7480,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )
bucket = conn.get_bucket('versionbugfix')
# bucket.configure_versioning(False)
# bucket.configure_versioning(True)
print "version status:",bucket.get_versioning_status()
print "=====================version test==========================="
for key in bucket.list_versions():
        print "{name}\t{modified}\t{version_id}".format(
                name = key.name,
                modified = key.last_modified,
                version_id=key.version_id,
                )
#bucket.delete_key(key.name)
#bucket.delete_key(key.name,version_id=key.version_id)
