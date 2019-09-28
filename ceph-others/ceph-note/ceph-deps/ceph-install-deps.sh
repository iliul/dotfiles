rm -rf $PWD/deps
mkdir  $PWD/deps
yum install --installroot=$PWD/deps --downloadonly ceph-radosgw ceph ceph-deploy
