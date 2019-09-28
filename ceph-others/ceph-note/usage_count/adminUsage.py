# -*- coding: UTF-8 -*-
from rgwadmin import *
from requests_toolbelt.utils import dump
import logging
import sys
from datetime import *
import math
logging.basicConfig(level=logging.DEBUG)
rgw = RGWAdmin(access_key='admin', secret_key='admin', server='yuliyangdebugweb68.tunnel.qydev.com',secure=False)


print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now().replace(minute=0,second=0,microsecond=0)-timedelta(hours=1))
print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now() - timedelta(hours=8))
print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now() - timedelta(hours=16))

response = rgw.get_usage(uid='date2', show_summary=True, show_entries=True,
                         start='{:%Y-%m-%d %H:%M:%S}'.format(datetime.now().replace(minute=0,second=0,microsecond=0)-timedelta(hours=1)),
                         )
print response
