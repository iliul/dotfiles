```
journalctl -b -f -u  ceph-rest-api
```
fast scp
```
tar -c bcsds_installer/ |pigz -p 16|ssh -c arcfour128 -o"MACs umac-64@openssh.com" 192.168.153.109  "gzip -d|tar -xC /root/test/"
```

```
[root@ceph13 ~]# ethtool bond4 |grep Speed
	Speed: 20000Mb/s
[root@ceph13 ~]# ethtool bond1 |grep Speed
	Speed: 1000Mb/s

```


```
yum groupinstall "GNOME Desktop"
# yum groupinstall 'KDE' 'X Window System'
Update default target
Once the above installation is complete, instruct CentOS 7 system to boot into a graphical target by default:
# systemctl set-default graphical.target
Removed symlink /etc/systemd/system/default.target.
Created symlink from /etc/systemd/system/default.target to /usr/lib/systemd/system/graphical.target.


yum install tigervnc-server -y
vncpasswd #设置密码
vncserver :1
vncserver -geometry 1920x1200   
vncserver -geometry 1680x1050  
vncserver -geometry 1366x768
vncconfig -nowin&
```

```
yum install privoxy
vim /etc/privoxy/config
systemctl start privoxy
forward-socks5   /               127.0.0.1:1080 .
listen-address 127.0.0.1:7777
```

```
[root@ceph13 devstack]# ip route add 10.128.3.0/24 via 10.142.50.254
```

http://vasir.net/blog/ubuntu/replace_string_in_multiple_files
```
grep -rl yum openstack/ | xargs sed -i 's/yum/proxychains yum/g'
```


cat  /etc/systemd/system/vncserver@\:3.service
```
[Unit]
Description=Remote desktop service (VNC)
After=syslog.target network.target

[Service]
Type=forking
# Clean any existing files in /tmp/.X11-unix environment
ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill :3 > /dev/null 2>&1 || :'
ExecStart=/usr/sbin/runuser -l onest -c "/usr/bin/vncserver :3 -geometry 1680x1050"
PIDFile=/home/onest/.vnc/%H%i.pid
ExecStop=/bin/sh -c '/usr/bin/vncserver -kill :3 > /dev/null 2>&1 || :'

[Install]
WantedBy=multi-user.target

```

random 1.1GiB
```
openssl rand -out 1.1GiB.bin  -base64 $(( 2**30 * 3/4 ))
```


python venv
```
import os,sys
sys.path.insert(1,os.path.join(os.path.abspath('.'),'venv/lib/python2.7/site-packages'))
```

sshfs mount
```
sshfs -o workaround=nodelaysrv:buflimit -o no_check_root -o kernel_cache -o auto_cache -o reconnect root@10.142.50.24:/usr/lib/python2.7/site-packages/cinder  /root/openstack/tmp

sshfs -o workaround=nodelaysrv:buflimit -o no_check_root -o kernel_cache -o auto_cache -o reconnect -o IdentityFile=/home/yuliyang/id_rsa  stack@10.140.0.3:/opt/stack/cinder/cinder  /home/yuliyang/cinder
```

sshfs umount
```
fusermount -u /root/yuliyang/development/openstack/ceph24
```

route
```
在128的机器上：route add -net 10.142.50.0/24 gw 10.128.3.254
在142的机器上：route add -net 10.128.3.0/24 gw 10.142.50.254
[root@ceph13 ~]# cat  /etc/sysconfig/network-scripts/route-bond4
10.133.0.0/16 via 10.142.50.254 dev bond4
10.139.0.0/16 via 10.142.50.254 dev bond4
172.16.0.0/16 via 10.142.50.254 dev bond4
10.128.3.0/24 via 10.142.50.254 dev bond4
```

xarg
```
for i in `seq 1 100`;do echo $i;done | xargs -n 1 -P 100  sh -c  'curl http://10.128.3.240:7480'
```

bond
```
[root@ceph35 ~]# cat  /etc/sysconfig/network-scripts/ifcfg-bond1
DEVICE=bond1
TYPE=Ethernet
ONBOOT=yes
NM_CONTROLLED=no
BOOTPROTO=static
BONDING_OPTS="mode=1 miimon=100"
IPADDR=10.254.9.35
NETMASK=255.255.255.0
GATEWAY=10.254.9.254

[root@ceph35 ~]# cat  /etc/sysconfig/network-scripts/ifcfg-enp130s0f0
DEVICE=enp130s0f0
BOOTPROTO=none
ONBOOT=yes
TYPE=Ethernet
NM_CONTROLLED=no
MASTER=bond1
SLAVE=yes


[root@ceph35 ~]# cat  /etc/sysconfig/network-scripts/ifcfg-enp130s0f1
DEVICE=enp130s0f1
BOOTPROTO=dhcp
ONBOOT=no
TYPE=Ethernet
NM_CONTROLLED=no


[root@ceph35 ~]# cat  /etc/sysconfig/network-scripts/ifcfg-bond4
DEVICE=bond4
TYPE=Bond
BONDING_MASTER=yes
ONBOOT=yes
BOOTPROTO=static
BONDING_OPTS="miimon=100 undelay=0 downdelay=0 mode=802.3ad xmit_hash_policy=2"
NAME=bond4
IPADDR=10.142.50.35
NETMASK=255.255.255.0



[root@ceph35 ~]# cat  /etc/sysconfig/network-scripts/ifcfg-enp2s0f0
TYPE=Ethernet
BOOTPROTO=none
UUID=4e1575f7-7ec2-4ebd-8ebc-90161908467a
DEVICE=enp2s0f0
ONBOOT=yes
NM_CONTROLLED=yes
MASTER=bond4
SLAVE=yes
[root@ceph35 ~]# cat  /etc/sysconfig/network-scripts/ifcfg-enp2s0f1
TYPE=Ethernet
BOOTPROTO=none
UUID=d986d92c-ad07-4634-8daa-dc1c15319616
DEVICE=enp2s0f1
ONBOOT=yes
NM_CONTROLLED=yes
MASTER=bond4
SLAVE=yes


[root@ceph35 ~]# cat  /etc/sysconfig/network-scripts/route-bond1
172.16.0.0/16 via 10.254.9.254
[root@ceph35 ~]# cat  /etc/sysconfig/network-scripts/route-bond4
172.16.0.0/16 via 10.142.50.254 dev bond4
10.128.3.0/24 via 10.142.50.254 dev bond4

```

PATH 
```
export PATH=$PATH:/path/to/dir
```

```
sudo apt-get install ttf-wqy-microhei  #文泉驿-微米黑
sudo apt-get install ttf-wqy-zenhei  #文泉驿-正黑
sudo apt-get install xfonts-wqy #文泉驿-点阵宋体
```

ubuntu static ip
```
auto eth1
iface eth1 inet static
address 192.168.153.101
netmask 255.255.255.0
```
