#!/usr/bin/env bash
KEY_ACCESS=$1
KEY_SECRET=$2
relativePath=$3
current=`TZ=GMT LANG=en_US date "+%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="GET\n\n\n${current}\n${relativePath}"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`
HOST=$4
curl -s -X GET "http://${HOST}$5" \
-H "Authorization: AWS ${KEY_ACCESS}:${signature}" \
-H "Date: ${current}" \
-H "Host: ${HOST}"




#./usage2.sh admin admin  '/admin/bucket' '127.0.0.1:7480'  '/admin/bucket?format=json&stats=true&bucket=fushitongbucket'
