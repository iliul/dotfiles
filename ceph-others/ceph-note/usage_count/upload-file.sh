#!/usr/bin/env bash
KEY_ACCESS="date2"
KEY_SECRET="date2"
file="/root/1G"
content_type=`file --mime-type $file | awk '{print $2}'`
BUCKET="07_22.19_03_05"
BUCKET="2016-07-23.11-28-43-033898CST"
OBJECT="1G-15"
relativePath="/${BUCKET}/${OBJECT}"
current=`TZ=GMT LANG=en_US date "+%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="PUT\n\n$content_type\n${current}\n${relativePath}"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`
#HOST="yuliyangdebugwebjewel.tunnel.qydev.com"
HOST="127.0.0.1:7480"
curl -v -X PUT -T "${file}" \
-H "Authorization: AWS ${KEY_ACCESS}:${signature}" \
-H "Date: ${current}" \
-H "Host: ${HOST}" \
-H "Expect:" \
-H "Content-Type: $content_type" \
"http://${HOST}${relativePath}"
