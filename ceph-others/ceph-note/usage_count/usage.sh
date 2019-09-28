#!/usr/bin/env bash
KEY_ACCESS="admin"
KEY_SECRET="admin"
relativePath="/admin/usage"
current=`TZ=GMT LANG=en_US date "+%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="GET\n\n\n${current}\n${relativePath}"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`
HOST="127.0.0.1:7480"
curl -s -v -X GET "http://${HOST}${relativePath}?format=json&uid=date2&start=$1&show-entries=True&show-summary=True" \
-H "Authorization: AWS ${KEY_ACCESS}:${signature}" \
-H "Date: ${current}" \
-H "Host: ${HOST}"
