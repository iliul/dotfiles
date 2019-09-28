http://dasheyuan.com/post/openstack-dev-environment/

http://chenyingkof.iteye.com/blog/2233315

http://blog.csdn.net/wenwenxiong/article/details/52700833

http://yikun.github.io/2016/02/23/%E4%BC%98%E9%9B%85%E5%9C%B0%E8%B0%83%E8%AF%95OpenStack/

https://osxfuse.github.io/

sshfs stack@192.168.35.10:/opt/stack /Users/yuliyang/openstack/code

eventlet.monkey_patch(all=False, socket=True, time=True, thread=False)

```
proxychains git clone https://git.openstack.org/openstack-dev/devstack -b stable/newton
./tools/create-stack-user.sh


[stack@devstack devstack]$ cat ~/.pip/pip.conf
[global]
default-timeout = 60
index-url = https://pypi.python.org/simple/

[install]
index-url = https://pypi.python.org/simple/


/etc/yum.conf
keepcache=1



sudo proxychains yum install -y https://www.rdoproject.org/repos/rdo-release.rpm
sudo yum makecache
sudo proxychains yum remove mariadb-libs mariadb mariadb-common mariadb-config -y
sudo proxychains yum install python-pip gcc openssl-devel python-psycopg2 postgresql-devel screen memcached mariadb-server ebtables bridge-utils -y
sudo proxychains pip install --upgrade pip
sudo proxychains pip install -U os-testr

export http_proxy=http://192.168.153.1:7777
export https_proxy=http://192.168.153.1:7777
export no_proxy=127.0.0.1,192.168.153.159

vi local.conf
[[local|localrc]]
DEST=/opt/stack
DOWNLOAD_DEFAULT_IMAGES=False
IMAGE_URLS="http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img"
HOST_IP=192.168.153.159
SERVICE_IP_VERSION=4
FLAT_INTERFACE=ens33
FLOATING_RANGE="192.168.153.0/24"
FIXED_RANGE="10.0.0.0/24"
Q_FLOATING_ALLOCATION_POOL=start=192.168.153.102,end=192.168.153.110
#PUBLIC_INTERFACE=ens33
PUBLIC_NETWORK_GATEWAY="192.168.153.1"
LIBVIRT_TYPE = qemu

RECLONE=no
GIT_BASE=http://git.trystack.cn
NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git
ENABLE_IDENTITY_V2=True

#OFFLINE=True
RECLONE=no
HORIZON_BRANCH=stable/newton
KEYSTONE_BRANCH=stable/newton
NOVA_BRANCH=stable/newton
NEUTRON_BRANCH=stable/newton
GLANCE_BRANCH=stable/newton
CINDER_BRANCH=stable/newton
NOVNC_BRANCH=v0.6.2

ADMIN_PASSWORD=openstack
DATABASE_PASSWORD=openstack
RABBIT_PASSWORD=openstack
SERVICE_PASSWORD=$ADMIN_PASSWORD
LOGDIR=$DEST/logs
LOGFILE=$DEST/logs/stack.sh.log
LOGDAYS=2

ENABLED_SERVICES=rabbit,mysql,key
ENABLED_SERVICES+=,n-api,n-crt,n-obj,n-cpu,n-cond,n-sch,n-novnc,n-cauth
ENABLED_SERVICES+=,g-api,g-reg
ENABLED_SERVICES+=,horizon
ENABLED_SERVICES+=,cinder,c-api,c-vol,c-sch,c-bak

# Neutron
DISABLED_SERVICES=n-net
ENABLED_SERVICES+=,q-svc,q-agt,q-dhcp,q-l3,q-meta,q-metering,neutron
PUBLIC_INTERFACE=eth0
Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True



This is your host IP address: 192.168.153.159
This is your host IPv6 address: ::1
Horizon is now available at http://192.168.153.159/dashboard
Keystone is serving at http://192.168.153.159/identity/
The default users are: admin and demo
The password: openstack
```


## yum repos
custum.repo

```
[base]
name=CentOS-$releasever - Base - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/os/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/os/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os
gpgcheck=0


#released updates
[updates]
name=CentOS-$releasever - Updates - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/updates/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/updates/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates
gpgcheck=0


#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/extras/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/extras/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras
gpgcheck=0


#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$releasever - Plus - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/centosplus/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/centosplus/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=centosplus
gpgcheck=0
enabled=0

#contrib - packages by Centos Users
[contrib]
name=CentOS-$releasever - Contrib - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/contrib/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/contrib/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=contrib
gpgcheck=0
enabled=0

[openstack]
name=openstack
baseurl=http://mirror.centos.org/centos/7/cloud/x86_64/openstack-newton/
enabled=1
gpgcheck=0
```

epel.repo
```
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
#baseurl=http://download.fedoraproject.org/pub/epel/7/$basearch
mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-7&arch=$basearch
failovermethod=priority
enabled=1
gpgcheck=0

[epel-debuginfo]
name=Extra Packages for Enterprise Linux 7 - $basearch - Debug
#baseurl=http://download.fedoraproject.org/pub/epel/7/$basearch/debug
mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-debug-7&arch=$basearch
failovermethod=priority
enabled=0
gpgcheck=0

[epel-source]
name=Extra Packages for Enterprise Linux 7 - $basearch - Source
#baseurl=http://download.fedoraproject.org/pub/epel/7/SRPMS
mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-source-7&arch=$basearch
failovermethod=priority
enabled=0
gpgcheck=0
```

epel-testing.repo
```
[epel-testing]
name=Extra Packages for Enterprise Linux 7 - Testing - $basearch
#baseurl=http://download.fedoraproject.org/pub/epel/testing/7/$basearch
mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=testing-epel7&arch=$basearch
failovermethod=priority
enabled=0
gpgcheck=0


[epel-testing-debuginfo]
name=Extra Packages for Enterprise Linux 7 - Testing - $basearch - Debug
#baseurl=http://download.fedoraproject.org/pub/epel/testing/7/$basearch/debug
mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=testing-debug-epel7&arch=$basearch
failovermethod=priority
enabled=0
gpgcheck=0

[epel-testing-source]
name=Extra Packages for Enterprise Linux 7 - Testing - $basearch - Source
#baseurl=http://download.fedoraproject.org/pub/epel/testing/7/SRPMS
mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=testing-source-epel7&arch=$basearch
failovermethod=priority
enabled=0
gpgcheck=0
```

```
This is your host IP address: 192.168.153.159
This is your host IPv6 address: ::1
Horizon is now available at http://192.168.153.159/dashboard
Keystone is serving at http://192.168.153.159/identity/
The default users are: admin and demo
The password: openstack
```

```
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=openstack
export OS_AUTH_URL="http://192.168.153.159:5000/v2.0"
export OS_ENDPOINT="http://192.168.153.159:35357/v2.0"
```
or
```
         project  user
. openrc  admin  admin
. openrc  admin  demo
. openrc  demo   demo
```

```
sudo iptables -I INPUT -s 0/0 -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT -s 0/0 -p tcp --dport 6080 -j ACCEPT
http://192.168.153.159/dashboard
admin
openstack

systemctl start httpd
systemctl enable httpd
screen -c devstack/stack-screenrc
openstack security group rule create --protocol tcp --dst-port 22 default  
openstack security group rule create --protocol icmp --dst-port -1 default


https://communities.cisco.com/community/developer/openstack/blog/2016/12/03/how-to-stack-devstack-newton-on-centos-7-in-virtualbox-on-mac
```
```
+-------------+----------------+--------------------------------------------------------------------------------+
| Name        | Type           | Endpoints                                                                      |
+-------------+----------------+--------------------------------------------------------------------------------+
| glance      | image          | RegionOne                                                                      |
|             |                |   publicURL: http://192.168.153.159:9292                                       |
|             |                |   internalURL: http://192.168.153.159:9292                                     |
|             |                |   adminURL: http://192.168.153.159:9292                                        |
|             |                |                                                                                |
| nova        | compute        | RegionOne                                                                      |
|             |                |   publicURL: http://192.168.153.159:8774/v2.1                                  |
|             |                |   internalURL: http://192.168.153.159:8774/v2.1                                |
|             |                |   adminURL: http://192.168.153.159:8774/v2.1                                   |
|             |                |                                                                                |
| nova_legacy | compute_legacy | RegionOne                                                                      |
|             |                |   publicURL: http://192.168.153.159:8774/v2/3824fdf4a57d436f8462cd41658ef929   |
|             |                |   internalURL: http://192.168.153.159:8774/v2/3824fdf4a57d436f8462cd41658ef929 |
|             |                |   adminURL: http://192.168.153.159:8774/v2/3824fdf4a57d436f8462cd41658ef929    |
|             |                |                                                                                |
| keystone    | identity       | RegionOne                                                                      |
|             |                |   publicURL: http://192.168.153.159/identity                                   |
|             |                |   internalURL: http://192.168.153.159/identity                                 |
|             |                |   adminURL: http://192.168.153.159/identity_v2_admin                           |
|             |                |                                                                                |
| neutron     | network        | RegionOne                                                                      |
|             |                |   publicURL: http://192.168.153.159:9696/                                      |
|             |                |   internalURL: http://192.168.153.159:9696/                                    |
|             |                |   adminURL: http://192.168.153.159:9696/                                       |
|             |                |                                                                                |
+-------------+----------------+--------------------------------------------------------------------------------+

```

![http://7o504d.com1.z0.glb.clouddn.com/tXNYvqK.png](http://7o504d.com1.z0.glb.clouddn.com/tXNYvqK.png)


pxe问题
```
#更新qemu版本
[root@ceph04 ~]# rpm -qa|grep qemu-kvm
qemu-kvm-common-ev-2.6.0-27.1.el7.x86_64
qemu-kvm-ev-2.6.0-27.1.el7.x86_64

yum install openstack-neutron-linuxbridge
```
