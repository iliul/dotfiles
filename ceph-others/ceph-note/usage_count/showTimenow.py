# -*- coding: utf-8 -*-
from datetime import *
print "当前时间（CST）：          ", '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
print "当前时间（CST）减去8小时： ", '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now() - timedelta(hours=8))
print "当前时间（CST）减去16小时：", '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now() - timedelta(hours=16))
str1 = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now() - timedelta(hours=8))
str2 = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now() - timedelta(hours=16))
print "----------------------------------------------------"
print "当前时间（CST）减去8小时： ",str1.replace(' ','%20')
print "当前时间（CST）减去16小时：",str2.replace(' ','%20')
