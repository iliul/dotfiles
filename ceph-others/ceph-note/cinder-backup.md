driver目录
```
[root@ceph04 yuliyang]# cd /usr/lib/python2.7/site-packages/cinder/backup/drivers/
[root@ceph04 drivers]# ls -l
total 352
-rw-r--r-- 1 root root 49688 Nov 17 02:21 ceph.py
-rw-r--r-- 2 root root 38859 Nov 17 02:30 ceph.pyc
-rw-r--r-- 2 root root 38859 Nov 17 02:30 ceph.pyo
-rw-r--r-- 1 root root  3480 Nov 17 02:21 glusterfs.py
-rw-r--r-- 2 root root  3400 Nov 17 02:30 glusterfs.pyc
-rw-r--r-- 2 root root  3400 Nov 17 02:30 glusterfs.pyo
-rw-r--r-- 1 root root 14327 Nov 17 02:21 google.py
-rw-r--r-- 2 root root 14878 Nov 17 02:30 google.pyc
-rw-r--r-- 2 root root 14878 Nov 17 02:30 google.pyo
-rw-r--r-- 1 root root     0 Nov 17 02:21 __init__.py
-rw-r--r-- 2 root root   153 Nov 17 02:30 __init__.pyc
-rw-r--r-- 2 root root   153 Nov 17 02:30 __init__.pyo
-rw-r--r-- 1 root root  3107 Nov 17 02:21 nfs.py
-rw-r--r-- 2 root root  3106 Nov 17 02:30 nfs.pyc
-rw-r--r-- 2 root root  3106 Nov 17 02:30 nfs.pyo
-rw-r--r-- 1 root root  5416 Nov 17 02:21 posix.py
-rw-r--r-- 2 root root  5389 Nov 17 02:30 posix.pyc
-rw-r--r-- 2 root root  5389 Nov 17 02:30 posix.pyo
-rw-r--r-- 1 root root 17026 Nov 17 02:21 swift.py
-rw-r--r-- 2 root root 14834 Nov 17 02:30 swift.pyc
-rw-r--r-- 2 root root 14834 Nov 17 02:30 swift.pyo
-rw-r--r-- 1 root root 20882 Nov 17 02:21 tsm.py
-rw-r--r-- 2 root root 16417 Nov 17 02:30 tsm.pyc
-rw-r--r-- 2 root root 16417 Nov 17 02:30 tsm.pyo

```
list and delete
```
[onest@ceph04 yuliyang]$ cinder backup-list
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+
| ID                                   | Volume ID                            | Status    | Name | Size | Object Count | Container     |
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+
| 461b51c1-7c9e-4c41-9f03-23cba4c0ef23 | ef3a93f7-c57b-4834-9f0e-6482fa9e1296 | available | -    | 1    | 22           | volumebackups |
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+
[onest@ceph04 yuliyang]$ cinder backup-delete 461b51c1-7c9e-4c41-9f03-23cba4c0ef23
Request to delete backup 461b51c1-7c9e-4c41-9f03-23cba4c0ef23 has been accepted.
[onest@ceph04 yuliyang]$ cinder backup-list
+----+-----------+--------+------+------+--------------+-----------+
| ID | Volume ID | Status | Name | Size | Object Count | Container |
+----+-----------+--------+------+------+--------------+-----------+
+----+-----------+--------+------+------+--------------+-----------+

```



vi /etc/cinder/cinder.conf
```
backup_swift_url = http://192.168.153.151/swift/v1/AUTH_
backup_swift_auth_url = http://192.168.153.151/auth
backup_swift_project = yuliyang
backup_swift_auth = single_user
backup_swift_auth_version = 1
backup_swift_user = yuliyang:swift
backup_swift_key = iRhOTDllsGyikWjefpjD575ZTfMCo2KDXJLrMs8N
backup_swift_container = volumebackups
backup_swift_object_size = 52428800  #50MB
backup_swift_block_size = 32768     #32KB
backup_swift_retry_attempts = 3
backup_swift_retry_backoff = 2
backup_compression_algorithm = zlib
```

ceph用户信息,无需配置ceph.conf,直接创建用户就可以了
```
[root@ceph01 ~]# radosgw-admin user info --uid=yuliyang
{
    "user_id": "yuliyang",
    "display_name": "yuliyang",
    "email": "",
    "suspended": 0,
    "max_buckets": 1000,
    "auid": 0,
    "subusers": [
        {
            "id": "yuliyang:swift",
            "permissions": "full-control"
        }
    ],
    "keys": [
        {
            "user": "yuliyang",
            "access_key": "yuliyang",
            "secret_key": "yuliyang"
        }
    ],
    "swift_keys": [
        {
            "user": "yuliyang:swift",
            "secret_key": "iRhOTDllsGyikWjefpjD575ZTfMCo2KDXJLrMs8N"
        }
    ],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "max_size_kb": -1,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "max_size_kb": -1,
        "max_objects": -1
    },
    "temp_url_keys": []
}

```


rbd backup
```
[ceph node]
ceph osd pool create backups 8
ssh 192.168.153.149 sudo tee /etc/ceph/ceph.conf </etc/ceph/ceph.conf   #192.168.153.149 is cinder-backup 
ceph auth get-or-create client.cinder-backup mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=backups'
ceph auth get-or-create client.cinder-backup | ssh 192.168.153.149 sudo tee /etc/ceph/ceph.client.cinder-backup.keyring
ssh 192.168.153.149 sudo chown cinder:cinder /etc/ceph/ceph.client.cinder-backup.keyring

[cinder-backup node]
yum install ceph

vi /etc/cinder/cinder.conf
backup_driver = cinder.backup.drivers.ceph
backup_ceph_conf = /etc/ceph/ceph.conf
backup_ceph_user = cinder-backup
backup_ceph_chunk_size = 134217728
backup_ceph_pool = backups
backup_ceph_stripe_unit = 0
backup_ceph_stripe_count = 0
restore_discard_excess_bytes = true
```

多个backup
```
cinder backup-create 3c4813bb-4fd1-4f5e-a577-2c1f6d5aa742 --container volumebackups --name test1
cinder backup-create 3c4813bb-4fd1-4f5e-a577-2c1f6d5aa742 --container backups --name test2
```


http://docs.ceph.com/docs/master/rbd/rbd-openstack/#create-a-pool


> 单独部署的cinder-backup(swift)如果要备份type=ceph的volume，cinder.conf也需要配置ceph,并且需要有对应的rpm包安装和/etc/ceph/下的keyring文件



[cinder volume & cinder backup node]
```
/etc/ceph/cinder-ceph.conf

[global]
fsid = 855385b9-7ff7-44d6-b479-2fe79885096d
max_open_files = 131072
mon_initial_members = ceph01
mon_host = 192.168.153.151
public_network = 192.168.153.0/24
cluster_network = 192.168.153.0/24

[client.cinder-backup]
keyring = /etc/ceph/ceph.client.cinder-backup.keyring

[client.cinder]
keyring = /etc/ceph/ceph.client.cinder.keyring
```



cinder调试环境快速搭建,虚拟机ubuntu16.04，推荐测试环境都用ubuntu
```
[[local|localrc]]
GIT_BASE=http://git.trystack.cn
NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git

ADMIN_PASSWORD=stack
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
MYSQL_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=111222333444

HOST_IP=10.140.0.3
SERVICE_HOST=$HOST_IP

OS_PROJECT_NAME=demo
OS_USERNAME=demo
OS_PASSWORD=password
OS_AUTH_URL=http://$SERVICE_HOST:5000/v2.0

DEST=/opt/stack
#RECLONE=yes
PIP_UPGRADE=True
#OFFLINE=True
VERSION=master
NOVNC_BRANCH=v0.6.2
#VERSION=stable/ocata
KEYSTONE_REPO=$GIT_BASE/openstack/keystone.git
KEYSTONE_BRANCH=$VERSION
CINDER_REPO=$GIT_BASE/openstack/cinder.git
CINDER_BRANCH=$VERSION
disable_all_services
enable_service mysql
enable_service rabbit
enable_service key
REGION_NAME=RegionOne
enable_service +=,cinder,c-api,c-vol,c-sch,c-bak
LOGFILE=$DEST/logs/stack.sh.log
LOGDIR=$DEST/logs
LOGDAYS=1
LOG_COLOR=False

```
