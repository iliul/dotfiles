```
[root@ceph05 ~]# cat  /etc/rsyslog.d/keepalived.conf
local7.* /var/log/keepalived.log

[root@ceph05 ~]# cat  /etc/sysconfig/keepalived
KEEPALIVED_OPTIONS="-f /var/log/keepalived.log -D -S 7"

sudo systemctl restart keepalived
sudo systemctl restart rsyslog
cat /var/log/keepalived.log | tail
```
