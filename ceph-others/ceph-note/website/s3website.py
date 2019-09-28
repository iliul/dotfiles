#!/usr/bin/env python2
import boto
import boto.s3.connection
import logging

sample_html = '''
<html>
  <head>
    <title>Sample "Hello, World" Application</title>
  </head>
  <body bgcolor=white>
    <h2>Yay! s3 websites </h2>
  </body>
</html>
'''

sample_error = '''
<html>
  <head>
    <title>Sample "Hello, World" Error</title>
  </head>
  <body bgcolor=white>
    <h2>Doh! something is wrong</h2>
  </body>
</html>
'''


from boto.s3.key import Key

if __name__ == '__main__':
    #main()
    akey = r'0555b35654ad1656d804'
    skey = r'h7GhxuBLTrlhVUyxSPUKUV8r/2EI4ngqJxD7iBdBYLhwluN30JaT3Q=='
    conn = boto.connect_s3(aws_access_key_id=akey,
                           aws_secret_access_key=skey,
                           is_secure=False,
                           host='127.0.0.1',
                           port=8000,
                           calling_format=boto.s3.connection.OrdinaryCallingFormat(),
                           debug=2)
    boto.set_stream_logger('boto')
    # create a bucket
    website_bucket = conn.create_bucket("website",policy='public-read')

    # upload index.html
    index_key = website_bucket.new_key('index.html')
    index_key.content_type = 'text/html'
    index_key.set_contents_from_string(sample_html, policy='public-read')

    # upload error page
    error_key = website_bucket.new_key('error.html')
    error_key.content_type = 'text/html'
    error_key.set_contents_from_string(sample_error, policy='public-read')


    website_bucket.configure_website('index.html','error.html')
    website_bucket.get_website_configuration()
