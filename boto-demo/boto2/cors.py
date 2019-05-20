import boto
import boto.s3.connection
from boto.exception import S3ResponseError
from boto.s3.cors import CORSConfiguration

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
        cb = self.conn.create_bucket(bucket_name)
        print("bucketName : {0}".format(cb.name))

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
        rb = self.conn.get_bucket(bucket_name)
        assert rb is not None
        print("get_bucket : {0}".format(rb.name))
        return rb


if __name__ == '__main__':
    conn = ConnectRadosGW(ACCESS_KEY, SECRET_KEY, HOST).conn()
    svc = S3BucketAction(conn)

    # S3 LIFECYCLE
    svc.create_bucket("s3-cors")
    bucket = svc.get_bucket("s3-cors")

    cors_cfg = CORSConfiguration()
    cors_cfg.add_rule(['PUT', 'POST', 'DELETE'], ['https://www.example.com'], allowed_header=['*'], max_age_seconds=3000,
                      expose_header=['x-amz-server-side-encryption'])
    cors_cfg.add_rule(['GET'], ['*'])

    # Set cors config
    bucket.set_cors(cors_cfg)

    # Get cors config
    print("bucket cors config = ", bucket.get_cors())

    # Delete cors config
    bucket.delete_cors()
