import aws_cdk
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_secretsmanager as sm,
    aws_kms as kms
)


class ParametersStoreStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        # aws ssm put-parameter --name "string-param" --type "String" --value "this-is-a-str-param-xx" [--overwrite]
        # aws ssm put-parameter --name "secure-string-param" --type "SecureString" --value "this-is-a-str-param-xx" [--overwrite]
        super().__init__(scope, construct_id, **kwargs)
        string_param = ssm.StringParameter.value_for_string_parameter(self, "string-param")
        sec_string_param = ssm.StringParameter.value_for_secure_string_parameter(self, "secure-string-param", 1)
        string_param_synth = ssm.StringParameter.value_from_lookup(self, "string-param")

        sec_string_param2 = aws_cdk.SecretValue.ssm_secure("secure-parameter", "1")

        #iam.User(self, "User", password=sec_string_param2)

        aws_cdk.CfnOutput(self, "parameter", value=string_param)
        aws_cdk.CfnOutput(self, "parameter_synth", value=string_param_synth)
        # aws_cdk.CfnOutput(self, "parameter_secure", value=sec_string_param)


        # ---------

        # aws kms list-keys
        # aws kms describe-key --key-id ed3013da-b560-4bbc-a976-a49deb0345ea # aws/secretsmanager managed key
        # aws secretsmanager create-secret --name user_psw --secret-string '{"sec": "a_sec_psw546"}' --kms-key-id ed3013da-b560-4bbc-a976-a49deb0345ea
        # aws secretsmanager update-secret --secret-id user_psw --secret-string '{"sec": "a_sec_psw546"}' --kms-key-id ed3013da-b560-4bbc-a976-a49deb0345ea

        key = kms.Key.from_key_arn(self, "kms-key", "arn:aws:kms:us-east-1:369871242120:key/ed3013da-b560-4bbc-a976-a49deb0345ea")
        #
        ssm_secret = sm.Secret.from_secret_attributes(self, "user_psw", encryption_key=key, secret_partial_arn="arn:aws:secretsmanager:us-east-1:369871242120:secret:user_psw")
        #
        secret_value = ssm_secret.secret_value.to_string()
        #aws_cdk.CfnOutput(self, "secret_man_str", value= secret_value)


