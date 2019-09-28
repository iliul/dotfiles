
# 安装openstack
```
使用安装脚本安装
https://github.com/tigerlinux/openstack-newton-installer-centos7
```
# 本地带GUI桌面的linux服务器

* 安装pycharm 专业版
* 安装sshfs   
```
sshfs -o workaround=nodelaysrv:buflimit -o no_check_root -o kernel_cache -o auto_cache -o reconnect root@cinder-24:/usr/lib/python2.7/site-packages/cinder  /root/openstack/tmp
```
* ssh -R 反向隧道(option,因为公司的物理机只能单向ping通)
