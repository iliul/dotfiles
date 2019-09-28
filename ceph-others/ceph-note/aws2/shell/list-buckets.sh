#!/usr/bin/env bash
KEY_ACCESS="admin"
KEY_SECRET="admin"
BUCKET=""
relativePath="/${BUCKET}"
current=`TZ=GMT LANG=en_US date "+%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="GET\n\n\n${current}\n${relativePath}"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`
HOST="yuliyangdebugwebjewel.tunnel.qydev.com"

curl -s -v -X GET "http://${HOST}${relativePath}" \
-H "Authorization: AWS ${KEY_ACCESS}:${signature}" \
-H "Date: ${current}" \
-H "Host: ${HOST}"



host=127.0.0.1:7480
# %08 is backspace
file=abc%08def
bucket=bucket-x
resource="/${bucket}/${file}"
contentType="text/plain"
dateValue=`date -R -u`
stringToSign="DELETE

${contentType}
${dateValue}
${resource}"
s3Key=aaaaa
s3Secret=bbbbb
signature=`/bin/echo -n "$stringToSign" | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -X DELETE \
  -H "Date: ${dateValue}" \
  -H "Content-Type: ${contentType}" \
  -H "Authorization: AWS ${s3Key}:${signature}" \
  http://${host}/${bucket}/$file
