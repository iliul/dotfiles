#!/usr/bin/env bash
KEY_ACCESS="admin"
KEY_SECRET="admin"
file="/root/admin2.py"
content_type=`file --mime-type $file | awk '{print $2}'`
BUCKET="create-by-curl"
OBJECT="OBJ3"
relativePath="/${BUCKET}/${OBJECT}"
current=`TZ=GMT LANG=en_US date "+%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="PUT\n\n$content_type\n${current}\n${relativePath}"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`
HOST="yuliyangdebugwebjewel.tunnel.qydev.com"
#HOST="192.168.10.10:7480"
curl -v -X PUT -T "${file}" \
-H "Authorization: AWS ${KEY_ACCESS}:${signature}" \
-H "Date: ${current}" \
-H "Host: ${HOST}" \
-H "Expect:" \
-H "Content-Type: $content_type" \
"http://${HOST}${relativePath}"
