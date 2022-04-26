#!/usr/bin/env python3
import os

import aws_cdk
import aws_cdk as cdk

import jsii

from cdk_sample.lambda_stack import LambdaStack
from cdk_sample.ecs_stack import EcsStack
from cdk_sample.vpc_stack import VpcStack
from cdk_sample.vpc2_stack import VPC2Stack
from cdk_sample.ec2_stack import Ec2Stack
from cdk_sample.parameters_store_stack import ParametersStoreStack
from cdk_sample.s3_stack import S3Stack
from cdk_sample.nested_stack import DemoStack


@jsii.implements(aws_cdk.IAspect)
class CheckTerminationProtection:
    def visit(self, stack):
        if isinstance(stack, aws_cdk.Stack):
            if not stack.termination_protection:
                cdk.Annotations.of(stack).add_warning("This stack has no termination protection enabled")


@jsii.implements(aws_cdk.IAspect)
class CheckS3Encryption:
    def visit(self, construct):
        if isinstance(construct, cdk.aws_s3.CfnBucket):
            if not construct.bucket_encryption:
                cdk.Annotations.of(construct).add_error("This bucket has no encryption enabled")


with open("./user_data/user_data.sh") as f:
    USER_DATA = f.read()

app = cdk.App()
lambda1s = LambdaStack(app, "LambdaStack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ[
                                                        "CDK_DEFAULT_REGION"]))  # env={'region': 'us-east-1'})

VPC2Stack(app, "VPC2Stack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))

s3s = S3Stack(app, "S3Stack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))

lambda1s.add_dependency(s3s) # adding dependencies

DemoStack(app, "DemoStack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))

ParametersStoreStack(app, "ParametersStoreStack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))

VPC = VpcStack(app, "VpcStack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))

EcsStack(app, "EcsStack", vpc=VPC.vpc, env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                           region=os.environ["CDK_DEFAULT_REGION"]))
Ec2Stack(app, "Ec2Stack",
         vpc=VPC.vpc,
         user_data=USER_DATA,
         env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                             region=os.environ["CDK_DEFAULT_REGION"])
         )

cdk.Aspects.of(app).add(CheckTerminationProtection())
cdk.Aspects.of(app).add(CheckS3Encryption())
app.synth()
