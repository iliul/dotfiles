删除rpm包
```
rpm -qa|grep 10.2 | awk '{system("yum remove " $1 " -y ")}' && rm -rf /etc/ceph /var/lib/ceph  /var/run/ceph 
```
