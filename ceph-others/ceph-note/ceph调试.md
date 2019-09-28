vstart启动集群
```
cd ceph/build
../src/vstart.sh -n -d --mon_num 1 --osd_num 3 --mds_num 0 --mgr_num 0 --rgw_num 1
```


```
gdbserver 127.0.0.1:8888 --attach 24457   #rgw pid
```

![](http://ww1.sinaimg.cn/large/006LGw6Ngy1fexlbeeqedj30vu094wi3.jpg)

```
下断点

s3cmd 模拟客户端操作

debug

```
