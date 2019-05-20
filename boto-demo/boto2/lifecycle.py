import boto
import boto.s3.connection
from boto.exception import S3ResponseError
from boto.s3.lifecycle import Expiration, Lifecycle, Transitions, Rule

ACCESS_KEY = 'xxx'
SECRET_KEY = 'xxxyyyzzz'
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
    svc.create_bucket("s3-lifecycle")
    bucket = svc.get_bucket("s3-lifecycle")

    # Transition rule
    transitions = Transitions()
    transitions.add_transition(days=3, storage_class='STANDARD_IA')
    # Expiration rule
    expiration = Expiration(days=7)
    rule = Rule(id='lc', prefix='logs/', status='Enabled', expiration=expiration, transition=transitions)

    lifecycle = Lifecycle()
    lifecycle.append(rule)

    # Set bucket lifecycle
    bucket.configure_lifecycle(lifecycle)

    # Get bucket lifecycle
    rl = bucket.get_lifecycle_config()
    print("Bucket lifecycle transition = ", rl[0].transition)
    print("Bucket lifecycle expiration = ", rl[0].expiration)

    # Delete bucket lifecycle
    bucket.delete_lifecycle_configuration()
