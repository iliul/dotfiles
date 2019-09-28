#!/usr/bin/env bash
KEY_ACCESS="admin"
KEY_SECRET="admin"
BUCKET="create-by-curl"
relativePath="/${BUCKET}"
current=`TZ=GMT LANG=en_US date "+%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="PUT\n\n\n${current}\n${relativePath}"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`
HOST="yuliyangdebugwebjewel.tunnel.qydev.com"

curl -s -v -X PUT "http://${HOST}${relativePath}" \
-H "Authorization: AWS ${KEY_ACCESS}:${signature}" \
-H "Date: ${current}" \
-H "Host: ${HOST}"
