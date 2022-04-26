from constructs import Construct
from aws_cdk import (
    NestedStack,
    Stack,
    Tags,
    aws_s3 as s3
)


class ANestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, bucket: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        Tags.of(self).add("S3TagName", "S3TagValue")
        self.bucket = s3.Bucket(self, "nested-bucket-id-{}".format(bucket),
                                bucket_name="demo-123122131235-{}".format(bucket),
                                encryption=s3.BucketEncryption.S3_MANAGED)

    @property
    def s3_arn(self):
        return self.bucket.bucket_arn


class DemoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        buckets = ["a-bucket", "b-bucket"]
        for bucket in buckets:
            ANestedStack(self, bucket, bucket=bucket)

