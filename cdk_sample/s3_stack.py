from constructs import Construct
from aws_cdk import (
    Stack,
    Tags,
    aws_s3 as s3
)


class S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        Tags.of(self).add("S3TagName", "S3TagValue")
        self.bucket = s3.Bucket(self, "a-bucket-123464456", encryption=s3.BucketEncryption.S3_MANAGED)

    @property
    def s3_arn(self):
        return self.bucket.bucket_arn
