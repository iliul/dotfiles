#pip install requesocks
import requesocks as requests
session = requests.session()
session.proxies = {
'http': 'socks5://127.0.0.1:1080',
'https': 'socks5://127.0.0.1:1080'
}
from awsauth import S3Auth
#host = "s3.amazonaws.com"
host = "s3-us-west-2.amazonaws.com"
access_key = 'xxx'
secret_key = 'xxx'
cmd = '/yuliyangtest2?location'
cmd = '/jwj-test-1?location'
cmd = '/regionj1?location'
# cmd = '/'
url = 'http://%s%s' % (host,cmd)
response = session.get(url, auth=S3Auth(access_key, secret_key,service_url=host))
print response.content
