#!/usr/bin/env bash
KEY_ACCESS="admin"
KEY_SECRET="admin"
file="/root/10M"
content_type=`file --mime-type $file | awk '{print $2}'`
BUCKET="testusage"
OBJECT="10M"
relativePath="/${BUCKET}/${OBJECT}"
current=`TZ=GMT LANG=en_US date "+%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="DELETE\n\n\n${current}\n${relativePath}"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`
#HOST="yuliyangdebugwebjewel.tunnel.qydev.com"
HOST="127.0.0.1:7480"
curl -s -v -X DELETE "http://${HOST}${relativePath}" \
-H "Authorization: AWS ${KEY_ACCESS}:${signature}" \
-H "Date: ${current}" \
-H "Host: ${HOST}"
