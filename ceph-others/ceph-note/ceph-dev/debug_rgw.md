由于主要关注rgw端，因此在rados直接使用rpm安装,ceph-radosgw模块编译调试


master branch
```
./bin/radosgw -f  -c /etc/ceph/ceph.conf --cluster ceph \
--name client.rgw.rgw1 --setuser ceph --setgroup ceph  \
--keyring /etc/ceph/keyring  --logfile /var/log/ceph-rgw.debug \
--debug-rgw 10/10  -m 192.168.153.156:6789
```
