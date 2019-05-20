# -*- coding:utf-8 -*-

import boto
import boto.s3.connection
from boto.exception import S3ResponseError

ACCESS_KEY = 'xxx'
SECRET_KEY = 'xxx'
HOST = 'oss-cn-beijing.speedycloud.org'


class ConnectRadosGW:
    def __init__(self, access_key, secret_key, host):
        self.access_key = access_key or ACCESS_KEY
        self.secret_key = secret_key or SECRET_KEY
        self.host = host or HOST

    def conn(self):
        s3 = boto.connect_s3(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            host=self.host,
            is_secure=False,
            calling_format=boto.s3.connection.OrdinaryCallingFormat(),
        )
        return s3


class S3BucketAction:
    def __init__(self, handler):
        self.conn = handler

    # create bucket
    def create_bucket(self, bucket_name):
        bucket = self.conn.create_bucket(bucket_name)
        print("bucketName : {0}".format(bucket.name))

    # head bucket
    def head_bucket(self, bucket_name):
        try:
            self.conn.head_bucket(bucket_name)
        except S3ResponseError as e:
            print("Bucket does not exist")

    # delete bucket
    def delete_bucket(self, bucket_name):
        self.conn.delete_bucket(bucket_name)

    # get bucket
    def get_bucket(self, bucket_name):
        bucket = self.conn.get_bucket(bucket_name)
        assert bucket is not None
        print("get_bucket : {0}".format(bucket.name))
        return bucket

    # create an object
    def create_object(self, bucket_name, object_name, content):
        bucket = self.get_bucket(bucket_name)
        assert bucket is not None
        key = bucket.new_key(object_name)
        key.set_contents_from_string(content)

    # delete an object
    def delete_object(self, bucket_name, object_name):
        bucket = self.get_bucket(bucket_name)
        assert bucket is not None
        bucket.delete_key(object_name)

    # change an object's acl
    def change_object_acl(self, bucket_name, object_name, acl):
        bucket = self.get_bucket(bucket_name)
        assert bucket is not None
        key = bucket.get_key(object_name)
        key.set_canned_acl(acl)

    # download an object to a file
    def download_object(self, bucket_name, object_name, file_name):
        bucket = self.get_bucket(bucket_name)
        assert bucket is not None
        try:
            key = bucket.get_key(object_name)
            key.get_contents_to_filename(file_name)
        except AttributeError as e:
            print("exception message : {0}".format(e))

    # object generate url
    def generate_url(self, bucket_name, object_name, expire_time=0, query_auth=False, force_http=True):
        bucket = self.get_bucket(bucket_name)
        assert bucket is not None
        key = bucket.get_key(object_name)
        assert key is not None
        key_url = key.generate_url(expire_time, query_auth=query_auth, force_http=force_http)
        print("key url : {0}".format(key_url))


if __name__ == '__main__':
    conn = ConnectRadosGW(ACCESS_KEY, SECRET_KEY, HOST).conn()
    s3Client = S3BucketAction(conn)

    # S3 INTERFACES
    s3Client.create_bucket("s3-boto")

    s3Client.create_object("s3-boto", "hello.txt", "some messages")

    s3Client.change_object_acl("s3-boto", "hello.txt", "private")

    s3Client.download_object("s3-boto", "hello.txt", "out.txt")

    s3Client.generate_url("s3-boto", "hello.txt", 0)
    s3Client.generate_url("s3-boto", "hello.txt", 3600, True)

    s3Client.delete_object("s3-boto", "hello.txt")

    s3Client.delete_bucket("s3-boto")
