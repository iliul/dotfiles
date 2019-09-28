## 时间同步
```
yum install -y chrony
systemctl start chronyd.service
systemctl restart chronyd.service
systemctl enable chronyd.service
#当服务器的话
allow 192.168/16

#开启防火墙
firewall-cmd --permanent --add-service=ntp
firewall-cmd --reload

#手动
chronyd -q 'server 0.asia.pool.ntp.org iburst'
chronyc sourcestats
chronyc sources -v
chronyc tracking

```
```
chronyc sources -v
date +%Y%m%d -s "20160616"
date +%T -s "8:55:30"
date -s "2016-06-21 16:42:00"
timedatectl set-timezone Asia/Shanghai
```

//设置ntp服务器本地
```
timedatectl set-timezone Asia/Shanghai

vi /etc/ntp.conf
restrict default nomodify
server  127.127.1.0     # local clock
fudge   127.127.1.0 stratum 8

//使用ntpdate客户端
server 192.168.10.5 iburst minpoll 4 maxpoll 4
```

## 查看硬盘使用量
```
df -lP | awk '{total+=$3} END {printf "%d G\n", total/2^20 + 0.5}'
for i in `seq 1 5`;do ssh ceph0$i df -lP | awk '{total+=$3} END {printf "%d G\n", total/2^20 + 0.5}';done
```

## 防火墙设置
```
systemctl disable firewalld
systemctl stop firewalld
sed -i  s'/SELINUX.*=.*enforcing/SELINUX=disabled'/g /etc/selinux/config
sed -i  s'/Defaults    requiretty/#Defaults    requiretty'/g /etc/sudoers
setenforce 0


firewall-cmd --list-all
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --reload


firewall-cmd --list-all
firewall-cmd --zone=public --remove-port=8080/tcp --permanent
firewall-cmd --reload

```

## 格式化磁盘
```
systemctl restart systemd-udevd.service
parted -a optimal --script /dev/sdk mklabel gpt
for sdd in `echo b c d e`;do parted -a optimal --script /dev/sd$sdd mklabel gpt ;done
parted -a optimal --script /dev/sdb mklabel gpt
```
## 添加用户
```
useradd -d /home/cephuser -m cephuser
passwd cephuser
echo "cephuser ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/cephuser
chmod 0440 /etc/sudoers.d/cephuser
sed -i 's/Defaults    requiretty/#Defaults    requiretty/g' /etc/sudoers
```

