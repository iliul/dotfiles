cat $1 | grep -e $2 -e "ceph-deploy"  | awk '{print $2}'| sort -k2n | awk '{if ($0!=line) print;line=$0}' > ceph.deps
cat $1 | grep  -v $2 | awk '{print $2}'| sort -k2n | awk '{if ($0!=line) print;line=$0}' > no-ceph.deps
