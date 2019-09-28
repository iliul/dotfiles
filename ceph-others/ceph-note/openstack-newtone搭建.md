
*** 有时出现因为网络无法创建vm，查看网卡是否改了！！！！！
*** 各个机器必须时间同步

|  IP  	| 192.168.153.148 	| 192.168.153.149 	| 192.168.153.150 	|
|:----:	|:---------------:	|:---------------:	|:---------------:	|
| ROLE 	|    CONTROLLER   	|      VOLUME     	|     COMPUTE     	|

修改/etc/hosts
```
127.0.0.1 localhost dev(当前主机名字)
192.168.153.148 controller
192.168.153.149 volume
192.168.153.150 compute
```
# base
[controller && volume && compute nodes]
```
yum -y install python-openstackclient openstack-selinux 
yum -y install crudini                      #ini格式配置文件修改工具
```
[controller node]
```
yum install rabbitmq-server -y
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
rabbitmqctl add_user openstack openstack
rabbitmqctl set_permissions openstack ".*" ".*" ".*"
yum install memcached python-memcached -y
systemctl enable memcached.service
systemctl start memcached.service
rabbitmq-plugins enable rabbitmq_management
```

部署 keystone,glance,nova,neutron[controller node]
```
yum install openstack-keystone httpd mod_wsgi -y
yum install openstack-glance -y
yum install openstack-nova-api openstack-nova-conductor  openstack-nova-console openstack-nova-novncproxy openstack-nova-scheduler -y
yum install openstack-neutron openstack-neutron-ml2 openstack-neutron-linuxbridge ebtables -y
```

数据库[controller node]
```
yum install mariadb mariadb-server python2-PyMySQL -y
touch /etc/my.cnf.d/openstack.cnf
crudini --set /etc/my.cnf.d/openstack.cnf mysqld bind-address 0.0.0.0
crudini --set /etc/my.cnf.d/openstack.cnf mysqld default-storage-engine innodb
crudini --set /etc/my.cnf.d/openstack.cnf mysqld max_connections 10000
crudini --set /etc/my.cnf.d/openstack.cnf mysqld collation-server utf8_general_ci
crudini --set /etc/my.cnf.d/openstack.cnf mysqld character-set-server utf8

systemctl enable mariadb.service
systemctl start mariadb.service
mysql_secure_installation
#
设置root密码为 openstack

mysql -uroot -popenstack -e "create database keystone;"
mysql -uroot -popenstack -e "grant all on keystone.* to 'keystone'@'localhost' identified by 'keystone';"
mysql -uroot -popenstack -e "grant all on keystone.* to 'keystone'@'%' identified by 'keystone';"
mysql -uroot -popenstack -e "create database glance;"
mysql -uroot -popenstack -e "grant all on glance.* to 'glance'@'localhost' identified by 'glance';"
mysql -uroot -popenstack -e "grant all on glance.* to 'glance'@'%' identified by 'glance';"
mysql -uroot -popenstack -e "create database nova;"
mysql -uroot -popenstack -e "grant all on nova.* to 'nova'@'localhost' identified by 'nova';"
mysql -uroot -popenstack -e "grant all on nova.* to 'nova'@'%' identified by 'nova';"
mysql -uroot -popenstack -e "create database nova_api;"
mysql -uroot -popenstack -e "grant all on nova_api.* to 'nova'@'localhost' identified by 'nova';"
mysql -uroot -popenstack -e "grant all on nova_api.* to 'nova'@'%' identified by 'nova';"
mysql -uroot -popenstack -e "create database neutron;"
mysql -uroot -popenstack -e "grant all on neutron.* to 'neutron'@'localhost' identified by 'neutron';"
mysql -uroot -popenstack -e "grant all on neutron.* to 'neutron'@'%' identified by 'neutron';"
mysql -uroot -popenstack -e "create database cinder;"
mysql -uroot -popenstack -e "grant all on cinder.* to 'cinder'@'localhost' identified by 'cinder';"
mysql -uroot -popenstack -e "grant all on cinder.* to 'cinder'@'%' identified by 'cinder';"
mysql -uroot -popenstack -e "FLUSH PRIVILEGES;"

#[option]enable root remote query
mysql -uroot -popenstack -e "grant all on *.* to 'root'@'%' identified by 'openstack';"
mysql -uroot -popenstack -e "FLUSH PRIVILEGES;"

```

[compute node]
```
yum install openstack-nova-compute -y
yum install openstack-neutron-linuxbridge ebtables ipset -y
```

配置keystone [controller node]
```
crudini --set /etc/keystone/keystone.conf database connection  mysql+pymysql://keystone:keystone@192.168.153.148/keystone
crudini --set /etc/keystone/keystone.conf token provider fernet

su -s /bin/sh -c "keystone-manage db_sync" keystone
keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
keystone-manage bootstrap --bootstrap-password admin --bootstrap-admin-url http://192.168.153.148:35357/v3/ --bootstrap-internal-url http://192.168.153.148:35357/v3/ --bootstrap-public-url http://192.168.153.148:5000/v3/ --bootstrap-region-id RegionOne

/etc/httpd/conf/httpd.conf
ServerName 192.168.153.148

ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/

systemctl enable httpd.service
systemctl restart httpd

export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_DOMAIN_NAME=default
export OS_AUTH_URL=http://192.168.153.148:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
```
```
openstack project create --domain default --description "Service Project" service
openstack project create --domain default --description "Demo Project" demo
openstack user create --domain default --password-prompt demo
openstack role create user
openstack role add --project demo --user demo user
```

配置glance [controller node]
```
openstack user create --domain default --password-prompt glance
openstack role add --project service --user glance admin
openstack service create --name glance --description "OpenStack Image" image
openstack endpoint create --region RegionOne image public http://192.168.153.148:9292
openstack endpoint create --region RegionOne image internal http://192.168.153.148:9292
openstack endpoint create --region RegionOne image admin http://192.168.153.148:9292

crudini --set /etc/glance/glance-api.conf database connection mysql+pymysql://glance:glance@192.168.153.148/glance
crudini --set /etc/glance/glance-api.conf keystone_authtoken auth_uri http://192.168.153.148:5000
crudini --set /etc/glance/glance-api.conf keystone_authtoken auth_url http://192.168.153.148:35357
crudini --set /etc/glance/glance-api.conf keystone_authtoken memcached_servers 192.168.153.148:11211
crudini --set /etc/glance/glance-api.conf keystone_authtoken auth_type password
crudini --set /etc/glance/glance-api.conf keystone_authtoken project_domain_name default
crudini --set /etc/glance/glance-api.conf keystone_authtoken user_domain_name default
crudini --set /etc/glance/glance-api.conf keystone_authtoken project_name service
crudini --set /etc/glance/glance-api.conf keystone_authtoken username glance
crudini --set /etc/glance/glance-api.conf keystone_authtoken password glance
crudini --set /etc/glance/glance-api.conf paste_deploy flavor keystone
crudini --set /etc/glance/glance-api.conf glance_store stores file,http
crudini --set /etc/glance/glance-api.conf glance_store default_store file
crudini --set /etc/glance/glance-api.conf glance_store filesystem_store_datadir /var/lib/glance/images/

crudini --set /etc/glance/glance-registry.conf database connection mysql+pymysql://glance:glance@192.168.153.148/glance
crudini --set /etc/glance/glance-registry.conf keystone_authtoken auth_uri http://192.168.153.148:5000
crudini --set /etc/glance/glance-registry.conf keystone_authtoken auth_url http://192.168.153.148:35357
crudini --set /etc/glance/glance-registry.conf keystone_authtoken memcached_servers 192.168.153.148:11211
crudini --set /etc/glance/glance-registry.conf keystone_authtoken auth_type password
crudini --set /etc/glance/glance-registry.conf keystone_authtoken project_domain_name default
crudini --set /etc/glance/glance-registry.conf keystone_authtoken user_domain_name default
crudini --set /etc/glance/glance-registry.conf keystone_authtoken project_name service
crudini --set /etc/glance/glance-registry.conf keystone_authtoken username glance
crudini --set /etc/glance/glance-registry.conf keystone_authtoken password glance
crudini --set /etc/glance/glance-registry.conf paste_deploy flavor keystone

su -s /bin/sh -c "glance-manage db_sync" glance
systemctl enable openstack-glance-api.service openstack-glance-registry.service
systemctl start openstack-glance-api.service openstack-glance-registry.service
openstack image create "cirros"  --file cirros-0.3.4-x86_64-disk.img  --disk-format qcow2 --container-format bare  --public
openstack image list
```
配置nova [controller node]
```
openstack user create --domain default --password-prompt nova
openstack role add --project service --user nova admin
openstack service create --name nova --description "OpenStack Compute" compute
openstack endpoint create --region RegionOne compute public http://192.168.153.148:8774/v2.1/%\(tenant_id\)s
openstack endpoint create --region RegionOne compute internal http://192.168.153.148:8774/v2.1/%\(tenant_id\)s
openstack endpoint create --region RegionOne compute admin http://192.168.153.148:8774/v2.1/%\(tenant_id\)s

/etc/nova/nova.conf

[DEFAULT]
enabled_apis = osapi_compute,metadata
transport_url=rabbit://openstack:openstack@192.168.153.148
auth_strategy = keystone
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
[api_database]
connection=mysql+pymysql://nova:nova@192.168.153.148/nova_api
[database]
connection=mysql+pymysql://nova:nova@192.168.153.148/nova
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = nova
[vnc]
vncserver_listen = 192.168.153.148
vncserver_proxyclient_address = 192.168.153.148
[glance]
api_servers = http://192.168.153.148:9292
[oslo_concurrency]
lock_path = /var/lib/nova/tmp

su -s /bin/sh -c "nova-manage api_db sync" nova
su -s /bin/sh -c "nova-manage db sync" nova

systemctl enable openstack-nova-api.service openstack-nova-consoleauth.service openstack-nova-scheduler.service openstack-nova-conductor.service openstack-nova-novncproxy.service
systemctl start openstack-nova-api.service openstack-nova-consoleauth.service openstack-nova-scheduler.service openstack-nova-conductor.service openstack-nova-novncproxy.service
```

[compute node]
```
/etc/nova/nova.conf
[DEFAULT]
enabled_apis = osapi_compute,metadata
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
auth_strategy = keystone
transport_url = rabbit://openstack:openstack@192.168.153.148
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = nova
[vnc]
enabled = True
vncserver_listen = 0.0.0.0
vncserver_proxyclient_address = 192.168.153.150
novncproxy_base_url = http://192.168.153.148:6080/vnc_auto.html
[glance]
api_servers = http://192.168.153.148:9292
[oslo_concurrency]
lock_path = /var/lib/nova/tmp
[libvirt]
virt_type=qemu
#virt_type=kvm

systemctl enable libvirtd.service openstack-nova-compute.service
systemctl start libvirtd.service openstack-nova-compute.service
```
neutron 配置 [controller node]
```
nova service-list
nova service-list
openstack image list
openstack user create --domain default --password-prompt neutron
openstack role add --project service --user neutron admin
openstack service create --name neutron --description "OpenStack Networking" network
openstack endpoint create --region RegionOne network public http://192.168.153.148:9696
openstack endpoint create --region RegionOne network internal http://192.168.153.148:9696
openstack endpoint create --region RegionOne network admin http://192.168.153.148:9696 

/etc/neutron/neutron.conf

[database]
connection = mysql+pymysql://neutron:neutron@192.168.153.148/neutron

[DEFAULT]
core_plugin = ml2
notify_nova_on_port_status_changes = True
notify_nova_on_port_data_changes = True
auth_strategy = keystone
service_plugins =
transport_url = rabbit://openstack:openstack@192.168.153.148

[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = neutron
password = neutron

[nova]
auth_url = http://192.168.153.148:35357
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = nova
password = nova

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp


/etc/neutron/plugins/ml2/ml2_conf.ini
[ml2]
type_drivers = flat,vlan,gre,vxlan,geneve
tenant_network_types =
mechanism_drivers = linuxbridge
extension_drivers = port_security
[ml2_type_flat]
flat_networks = public
[securitygroup]
enable_ipset = True

/etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = public:eth0
physical_interface_mappings = public:bond4_1.1003  
[vxlan]
enable_vxlan = False
[securitygroup]
enable_security_group = True
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver

/etc/neutron/dhcp_agent.ini
[DEFAULT]
interface_driver = neutron.agent.linux.interface.BridgeInterfaceDriver
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = True

/etc/neutron/metadata_agent.ini
[DEFAULT]
nova_metadata_ip = 192.168.153.148
metadata_proxy_shared_secret = trying

/etc/nova/nova.conf
[neutron]
url = http://192.168.153.148:9696
auth_url = http://192.168.153.148:35357
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = neutron
password = neutron
service_metadata_proxy = True
metadata_proxy_shared_secret = trying

ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron

systemctl restart openstack-nova-api.service
systemctl enable neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service
systemctl start neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service
```

[compute node]
```
/etc/neutron/neutron.conf
[DEFAULT]
auth_strategy = keystone
transport_url = rabbit://openstack:openstack@192.168.153.148

[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = neutron
password = neutron

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp

/etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = public:ens34
[vxlan]
enable_vxlan = False
[securitygroup]
enable_security_group = True
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver

/etc/nova/nova.conf
[neutron]
url = http://192.168.153.148:9696
auth_url = http://192.168.153.148:35357
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = neutron
password = neutron

systemctl restart openstack-nova-compute.service
systemctl enable neutron-linuxbridge-agent.service
systemctl start neutron-linuxbridge-agent.service
```

[controller node]
```
neutron ext-list
neutron agent-list
neutron agent-list
```

[controller node]
```
openstack network create --share --provider-physical-network public --provider-network-type flat public
openstack subnet create --network public --allocation-pool start=192.168.150.200,end=192.168.150.230 --dns-nameserver 192.168.150.2 --gateway 192.168.150.2 --subnet-range 192.168.0.0/16 public-instance
```
[controller node]
```
openstack flavor create --id 0 --vcpus 1 --ram 64 --disk 1 m1.nano
openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey
openstack keypair list
openstack security group rule create --proto icmp default
openstack security group rule create --proto tcp --dst-port 22 default
[root@controller ~]# openstack flavor list
+----+---------+-----+------+-----------+-------+-----------+
| ID | Name    | RAM | Disk | Ephemeral | VCPUs | Is Public |
+----+---------+-----+------+-----------+-------+-----------+
| 0  | m1.nano |  64 |    1 |         0 |     1 | True      |
+----+---------+-----+------+-----------+-------+-----------+
[root@controller ~]# openstack network list
+--------------------------------------+--------+--------------------------------------+
| ID                                   | Name   | Subnets                              |
+--------------------------------------+--------+--------------------------------------+
| 3d536cb7-5a58-452f-a461-f12fd3129e52 | public | 3cb136e9-0315-4cd5-8be0-a7049d146732 |
+--------------------------------------+--------+--------------------------------------+
[root@controller ~]# openstack image list
+--------------------------------------+--------+--------+
| ID                                   | Name   | Status |
+--------------------------------------+--------+--------+
| d1ee6656-353e-42d8-8756-c5ed98fd7f02 | cirros | active |
+--------------------------------------+--------+--------+
[root@controller ~]#  openstack security group list
+--------------------------------------+---------+-------------+----------------------------------+
| ID                                   | Name    | Description | Project                          |
+--------------------------------------+---------+-------------+----------------------------------+
| a02d525b-9809-40ba-aeac-31cc067ba861 | default | 缺省安全组  | bb63988618664e3099be225e8b8fd485 |
+--------------------------------------+---------+-------------+----------------------------------+

openstack server create --flavor m1.nano --image cirros --nic net-id=3d536cb7-5a58-452f-a461-f12fd3129e52 --security-group default --key-name mykey public-instance
openstack server list
openstack console url show public-instance
```
[controller node]
```
openstack user create --domain default --password-prompt cinder
openstack role add --project service --user cinder admin
openstack service create --name cinder --description "OpenStack Block Storage" volume
openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2
openstack endpoint create --region RegionOne   volume admin http://192.168.153.148:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volume internal http://192.168.153.148:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volume public http://192.168.153.148:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volumev2 public http://192.168.153.148:8776/v2/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volumev2 internal http://192.168.153.148:8776/v2/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volumev2 admin http://192.168.153.148:8776/v2/%\(tenant_id\)s

yum install openstack-cinder -y
vi /etc/cinder/cinder.conf
[database]
connection = mysql+pymysql://cinder:cinder@192.168.153.148/cinder 
[DEFAULT]
transport_url = rabbit://openstack:openstack@192.168.153.148
auth_strategy = keystone
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = cinder
password = cinder
[oslo_concurrency]
lock_path = /var/lib/cinder/tmp

iscsi_ip_address = 192.168.153.148

su -s /bin/sh -c "cinder-manage db sync" cinder
/etc/nova/nova.conf
[cinder]
os_region_name = RegionOne

systemctl restart openstack-nova-api.service
systemctl enable openstack-cinder-api.service openstack-cinder-scheduler.service
systemctl start openstack-cinder-api.service openstack-cinder-scheduler.service
```

[compute node]
```
/etc/nova/nova.conf
[cinder]
os_region_name = RegionOne
```

[volume node]
```
yum install lvm2
systemctl enable lvm2-lvmetad.service
systemctl start lvm2-lvmetad.service

[root@volume ~]# lsblk -f
NAME                         FSTYPE      LABEL UUID                                   MOUNTPOINT
fd0
sda
├─sda1                       ext4              d0f7f2b7-d7f6-47b8-81ee-e7365711a4ba   /boot
└─sda2                       LVM2_member       qYShvG-Xirl-wLST-j0gU-iXPk-34Qx-15mSKA
  ├─bclinux-root             ext4              4e448946-20a4-40c4-a9c6-7f5c12d94bc2   /
  ├─bclinux-swap             swap              ef5c4b36-c315-43ff-a9d4-ff0fe796bf8f   [SWAP]
  └─bclinux-docker--poolmeta
sdb


/etc/lvm/lvm.conf 修改filter
[root@volume ~]# pvcreate /dev/sdb
  Physical volume "/dev/sdb" successfully created

[root@volume ~]# vgcreate cinder-volumes /dev/sdb
  Volume group "cinder-volumes" successfully created

如果出现 pvcreate /dev/sdb Device /dev/sdb not found (or ignored by filtering).
[onest@ceph04 yuliyang]$ sudo dd if=/dev/urandom of=/dev/sdb bs=512 count=64
64+0 records in
64+0 records out
32768 bytes (33 kB) copied, 0.0034822 s, 9.4 MB/s
[onest@ceph04 yuliyang]$ sudo pvcreate /dev/sdb
  Physical volume "/dev/sdb" successfully created

sudo dd if=/dev/urandom of=/root/dir/512MiB  bs=1M count=51
  
  
yum install openstack-cinder targetcli python-keystone -y

/etc/cinder/cinder.conf
[DEFAULT]
glance_api_servers = http://192.168.153.148:9292
auth_strategy = keystone
enabled_backends = lvm
transport_url = rabbit://openstack:openstack@192.168.153.148
[oslo_concurrency]
lock_path = /var/lib/cinder/tmp
[database]
connection = mysql+pymysql://cinder:cinder@192.168.153.148/cinder
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = cinder
password = cinder

iscsi_ip_address = 192.168.153.149
[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
iscsi_protocol = iscsi
iscsi_helper = lioadm

systemctl enable openstack-cinder-volume.service target.service
systemctl start openstack-cinder-volume.service target.service

[root@controller ~]# iptables -I INPUT -s 0/0 -p tcp --dport 3306 -j ACCEPT
```

[controller node]
```
openstack volume service list
#1G
openstack volume create --size 1 volume1
openstack server add volume public-instance volume1
sudo mkfs.ext4 /dev/vdb
openstack server remove volume public-instance volume1
```

## 部署好后的常用管理命令
```
openstack catalog list
openstack volume service list
openstack server list
neutron agent-list
nova service-list
systemctl start rabbitmq-server.service
systemctl start memcached.service
systemctl start mariadb.service
systemctl start openstack-glance-api.service openstack-glance-registry.service
systemctl start openstack-nova-api.service openstack-nova-consoleauth.service openstack-nova-scheduler.service openstack-nova-conductor.service openstack-nova-novncproxy.service
systemctl start libvirtd.service openstack-nova-compute.service
systemctl start neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service
systemctl start neutron-linuxbridge-agent.service
systemctl start openstack-cinder-api.service openstack-cinder-scheduler.service
systemctl start lvm2-lvmetad.service
systemctl start openstack-cinder-volume.service target.service
systemctl start openstack-cinder-backup.service

[cinder-volume]
tgt-admin --show

[compute]
[stack@devstack devstack]$ sudo virsh list
 Id    名称                         状态
----------------------------------------------------
 1     instance-00000001              running
 2     instance-00000002              running

```
## iptable设置
```
yum install iptables-services
systemctl enable iptables
systemctl disable firewalld
service iptables restart
```

去除 cinder service 
```
cinder-manage service  remove cinder-volume controller
```
重启后volume卷无法挂载
```
[volume]
targetcli ls
systemctl stop firewalld
systemctl start iscsid
systemctl enable iscsid


[computer]
telnet 192.168.150.148 3260
```

ceph swift配置keystone支持
```
rgw_keystone_admin_user = admin
rgw_keystone_admin_password = openstack
rgw_keystone_admin_tenant = admin
rgw_keystone_accepted_roles = admin, Member, swiftoperator
rgw_keystone_url = http://192.168.153.142:5000
rgw_keystone_token_cache_size = 100
rgw_keystone_revocation_interval = 600
rgw_s3_auth_use_keystone = true
```
配置文件工具
```
crudini --set $CONFIG_FILE database connection mysql://nova:nova@$(hostname -i)/nova
crudini --set $CONFIG_FILE keystone_authtoken auth_uri http://$(hostname -i):5000/v2.0
```


# cinder操着
```
#enable and disable
cinder service-enable volume cinder-backup
cinder service-disable volume@lvm cinder-volume

cinder type-create ceph
cinder type-create lvm
cinder type-key ceph set volume_backend_name=ceph
cinder type-key lvm set volume_backend_name=lvm
cinder extra-specs-list

cinder create --volume_type ceph --display_name vol-ceph3 1

/etc/cinder/cinder.conf
enabled_backends = lvm,ceph
[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
volume_backend_name=lvm
iscsi_protocol = iscsi
iscsi_helper = lioadm
[ceph]
volume_driver = cinder.volume.drivers.rbd.RBDDriver
volume_backend_name=ceph
rbd_pool = volumes
rbd_ceph_conf = /etc/ceph/ceph.conf
rbd_flatten_volume_from_snapshot = false
rbd_max_clone_depth = 5
rbd_store_chunk_size = 4
rados_connect_timeout = -1
glance_api_version = 2
rbd_user = cinder
rbd_secret_uuid = 457eb676-33da-42ec-9a8c-9293d545c337

ceph auth get-or-create client.cinder | ssh {your-volume-server} sudo tee /etc/ceph/ceph.client.cinder.keyring
ssh {your-cinder-volume-server} sudo chown cinder:cinder /etc/ceph/ceph.client.cinder.keyring


[computer node]
vi /etc/nova/nova.conf
[libvirt]
rbd_user = cinder
rbd_secret_uuid = 457eb676-33da-42ec-9a8c-9293d545c337

systemctl restart openstack-nova-compute.service 
```

#创建loop0 lvm
```
#!/bin/sh
function truncate_file()
{
    local f=$1
    # calc wanted size
    size=$(df -P -k $(dirname $f)|tail -1| \
                  perl -ne 'm/^\S+\s*\d+\s+\d+\s+(\d+)/; print int($1*0.3)')

    if [ $size -le 2000000 ] ; then
        echo "error detecting free space or FS too small: $size KB"
        exit 12
    fi
    truncate --size=${size}K $f
}

function setup_vg()
{
    local vg_name=$1
    local vg_dev=$2
    local loop_file=$3

    vgchange -an $vg_name
    if [ -n "$loop_file" ] && [ ! -e "$loop_file" ] ; then
        truncate_file $loop_file
        losetup $vg_dev $loop_file
    fi

    pvcreate $vg_dev
    vgcreate $vg_name $vg_dev
    vgchange -ay $vg_name

    echo "using device $vg_dev for VG $vg_name"
}

####################
# script starts here
####################
systemctl enable lvm2-lvmetad
systemctl start lvm2-lvmetad

modprobe loop

# enable or create cinder-volumes VG
if vgs |grep -q cinder-volumes ; then
  echo "using existing cinder-volumes VG"
  vgchange -ay cinder-volumes
else
    # create new VG
    dev="/dev/loop0"
    loop_file="/var/lib/cinder/volumes-pv"
    if [ -n "$CINDER_VOLUMES_DEV" ]; then
        dev=$CINDER_VOLUMES_DEV
        loop_file=""
    fi
    setup_vg "cinder-volumes" "$dev" "$loop_file"
fi
```

```
ovs-vsctl del-port br-bond1 bond1
ovs-vsctl del-br br-tun
ovs-vsctl del-br br-int
ovs-vsctl del-br br-ex
systemctl stop openvswitch.service
systemctl disable openvswitch.service
systemctl stop openvswitch-nonetwork.service
systemctl disable openvswitch-nonetwork.service
rmmod openvswitch
```

