```
~/.bashrc
alias json="python -mjson.tool"
alias xml="xmllint --format -"


apt-get install libxml2-utils
```

```
git difftool --extcmd icdiff


icdiff  file1 file2
git difftool --extcmd icdiff 08f83c3a9ee4913a08760a332c289568300825b7^ 08f83c3a9ee4913a08760a332c289568300825b7 

```

ss隧道
```
场景1：有跳板机

uselocalss_jump_step1.bat 
#建立隧道，访问跳板机器（192.168.10.202）的1080就是访问本机(执行该bat文件的机器)的1080，本机使用ss window客户端
plink.exe -N -C -R 0.0.0.0:1080:127.0.0.1:1080  root@192.168.10.202  -pw 跳板机器密码

uselocalss_jump_step2.bat
#建立隧道，192.168.10.201 访问 192.168.10.201 的1080端口就是访问跳板机器的1080端口
# !!!! >>>>>>>>>>>>---- 192.168.10.202到 192.168.10.201做免密钥登陆 ---->>>>>>>>>>>>>>>>>!!!!
plink.exe  root@192.168.10.202  -pw 跳板机器密码 "ssh -CNR 1080:127.0.0.1:1080 root@192.168.10.201"

于是 192.168.10.201 的proxychain 访问 127.0.0.1:1080就是走window ss客户端的代理

场景2：无跳板机

plink.exe -N -C -R 0.0.0.0:1080:127.0.0.1:1080  root@192.168.10.201  -pw 跳板机器密码
```
uselocalss_without_jump.bat
```
plink.exe -N -C -R 0.0.0.0:1080:127.0.0.1:1080  root@10.142.50.36  -pw qwe123
```
uselocalss_jump_step1.bat
```
plink.exe -N -C -R 0.0.0.0:1080:127.0.0.1:1080  root@192.168.10.202  -pw qwe123
```
uselocalss_jump_step2.bat
```
plink.exe  root@192.168.10.202  -pw qwe123 "ssh -CNR 1080:127.0.0.1:1080 root@192.168.10.201"
```
下载yum源
```
proxychains wget -r --no-parent --reject "*11.0.1*" --reject "*11.0.2*" --reject "*debug*"    https://download.ceph.com/rpm-kraken/el7/x86_64/  /root/yum/

yum install ceph --downloadonly --downloaddir=/root/download/
```
```
1、在ssh服务端上更改/etc/ssh/sshd_config文件中的配置为如下内容：
UseDNS no
# GSSAPI options
GSSAPIAuthentication no
然后，执行/etc/init.d/sshd restart重启sshd进程使上述配置生效，在连接一般就不慢了。
```
