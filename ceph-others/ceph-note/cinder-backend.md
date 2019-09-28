https://github.com/tigerlinux/tigerlinux-extra-recipes/blob/master/recipes/openstack/openstack-mitaka-with-ceph-backend/RECIPE-LAB-Ceph-Rados-Mitaka-PART2.md

```
cinder service-disable volume cinder-backup
cinder service-enable volume cinder-backup
cinder service-disable volume@lvm cinder-volume

openstack server add volume public-instance3 vol-ceph3
openstack server remove volume public-instance3 vol-ceph3


cinder backup-create 61d4aab0-a81e-4ef2-8806-0ffd2ad59806  --name from_rbd_b1 --force
cinder backup-list
cinder backup-delete 94fb00bb-0bdf-487a-867b-435c3011908a

openstack volume delete f3239565-d0c9-4516-9264-e82ef8b47b75
openstack volume list
cinder create --volume_type ceph --display_name vol-ceph3 1


```

```
[controller node]
cinder type-create ceph
cinder type-create lvm
cinder type-key ceph set volume_backend_name=ceph
cinder type-key lvm set volume_backend_name=lvm
cinder extra-specs-list
systemctl restart openstack-cinder-api.service openstack-cinder-scheduler.service


[volume node]
systemctl restart openstack-cinder-volume.service

[DEFAULT]
...
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


[cinder-backup node]
/etc/ceph/ceph.conf
[client.cinder]
keyring = /etc/ceph/cinder.keyring

[controller node]
[root@controller ~]# openstack volume service list
+------------------+-------------+------+---------+-------+----------------------------+
| Binary           | Host        | Zone | Status  | State | Updated At                 |
+------------------+-------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller  | nova | enabled | up    | 2017-02-04T03:00:18.000000 |
| cinder-volume    | volume@lvm  | nova | enabled | up    | 2017-02-04T03:00:19.000000 |
| cinder-backup    | volume      | nova | enabled | up    | 2017-02-04T03:00:14.000000 |
| cinder-backup    | controller  | nova | enabled | up    | 2017-02-04T03:00:15.000000 |
| cinder-volume    | volume@ceph | nova | enabled | up    | 2017-02-04T03:00:07.000000 |
+------------------+-------------+------+---------+-------+----------------------------+


[ceph node]
ceph auth get-or-create client.cinder | ssh {your-volume-server} sudo tee /etc/ceph/ceph.client.cinder.keyring
ssh {your-cinder-volume-server} sudo chown cinder:cinder /etc/ceph/ceph.client.cinder.keyring


[computer node]
vi /etc/nova/nova.conf
[libvirt]
rbd_user = cinder
rbd_secret_uuid = 457eb676-33da-42ec-9a8c-9293d545c337

systemctl restart openstack-nova-compute.service 


[volume node]
[root@volume ~]# vi  /etc/cinder/cinder.conf
[root@volume ~]# ls -l /etc/ceph/
总用量 24
-rw-------. 1 root   root     63 11月 30 23:29 ceph.client.admin.keyring
-rw-r--r--  1 cinder cinder   71 2月   3 14:51 ceph.client.cinder-backup.keyring
-rw-r--r--  1 cinder cinder   64 2月   4 11:25 ceph.client.cinder.keyring
-rwxrwxrwx. 1 root   root   3760 2月   3 14:46 ceph.conf
-rwxr-xr-x  1 root   root     92 9月  28 09:28 rbdmap
drwxr-xr-x  2 root   root   4096 12月  1 20:56 supervisord.d


[controller]
cinder create --volume_type ceph --display_name vol-ceph3 1
[root@controller ~]# openstack server add volume public-instance3 vol-ceph3
[root@controller ~]# openstack volume list
+--------------------------------------+-----------------+-----------+------+-------------------------------------------+
| ID                                   | Display Name    | Status    | Size | Attached to                               |
+--------------------------------------+-----------------+-----------+------+-------------------------------------------+
| 61d4aab0-a81e-4ef2-8806-0ffd2ad59806 | vol-ceph3       | in-use    |    1 | Attached to public-instance3 on /dev/vdd  |
| ca734f34-635c-43dd-82ea-c79b13863fc7 | volume-1G-rbd   | in-use    |    1 | Attached to public-instance3 on /dev/vdc  |
| f2aadd6f-b06f-4d7d-8459-f540486fc879 | volume-1G-swift | in-use    |    1 | Attached to public-instance3 on /dev/vdb  |
| 100c5db2-96c9-454c-a457-7f5edd46b22b | volume2         | available |    1 |                                           |
| f3239565-d0c9-4516-9264-e82ef8b47b75 | volume1         | available |    1 |                                           |
+--------------------------------------+-----------------+-----------+------+-------------------------------------------+
[root@controller ~]# ssh cirros@192.168.153.206
$ sudo lsblk -f
NAME   FSTYPE LABEL         MOUNTPOINT
vda
`-vda1 ext3   cirros-rootfs /
vdb    ext4                 /root/swift
vdc    ext4                 /root/rbd
vdd



```


```
[onest@ceph04 yuliyang]$ cat create_volume.sh
cinder create --volume_type $1 --display_name $2 $3

[onest@ceph04 yuliyang]$ cat attach_volume.sh
nova volume-attach 1eee9a3f-8eea-40bb-b403-5e3cd0a380be $1

[onest@ceph04 yuliyang]$ cat detach_volume.sh
nova volume-detach 1eee9a3f-8eea-40bb-b403-5e3cd0a380be $1

[onest@ceph04 yuliyang]$ cat enable-swift-backup-disable-rbd-backup.sh
cinder service-disable ceph04 cinder-backup
cinder service-enable ceph05 cinder-backup

[onest@ceph04 yuliyang]$ cat enable-rbd-backup-disable-swift-backup.sh
cinder service-disable ceph05 cinder-backup
cinder service-enable ceph04 cinder-backup

```
