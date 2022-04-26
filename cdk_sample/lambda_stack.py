from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_kms as kms,
    aws_secretsmanager as sm
)


class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(self, "lambda_role",
                        assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                        role_name="lambda_role"
                        )

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))

        key = kms.Key.from_key_arn(self, "kms-key",
                                   "arn:aws:kms:us-east-1:369871242120:key/ed3013da-b560-4bbc-a976-a49deb0345ea")
        ssm_secret = sm.Secret.from_secret_attributes(self, "user_psw", encryption_key=key,
                                                      secret_partial_arn="arn:aws:secretsmanager:us-east-1:369871242120:secret:user_psw")
        secret_value = ssm_secret.secret_value.unsafe_unwrap()

        hello_function = _lambda.Function(self,
                                          'WelcomeHAndler',
                                          runtime=_lambda.Runtime.PYTHON_3_9,
                                          code=_lambda.Code.from_asset('lambda-api'),
                                          environment={
                                              "A_SECRET": secret_value
                                          },
                                          handler='welcome.handler',
                                          role=role
                                          )

        apigw.LambdaRestApi(self, 'Endpoint', handler=hello_function)
