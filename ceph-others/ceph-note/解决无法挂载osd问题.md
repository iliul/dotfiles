
```
for i in `mount |grep osd | awk '{ print $3}' | awk  -F"/" '{print $NF}' | cut -d - -f2`;do systemctl enable ceph-osd@$i;done
```

```
#check
ansible -i nanji_slave_all_172.16.127  osds  -v -u root -a "ls -l  /etc/systemd/system/ceph-osd.target.wants/" -f 100
#do link
ansible-playbook activte-osd-link.yml -i nanji_slave_all_172.16.127 -v -u root -f 100
```

```
---
- hosts:
    - osds
  become: True
  tasks:
      - name: soft link
        shell: "ln -s /usr/lib/systemd/system/ceph-disk@.service /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sd{{ item }}1.service"
        with_items: [b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w]

```

```
[root@graphite ~]# ln -s /usr/lib/systemd/system/ceph-disk\@.service  /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sdb1.service
[root@graphite ~]# ln -s /usr/lib/systemd/system/ceph-disk\@.service  /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sdc1.service
[root@graphite ~]# ln -s /usr/lib/systemd/system/ceph-disk\@.service  /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sdd1.service
[root@graphite ~]# ln -s /usr/lib/systemd/system/ceph-disk\@.service  /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sde1.service
```
