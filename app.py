#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_sample.lambda_stack import LambdaStack
from cdk_sample.ecs_stack import EcsStack
from cdk_sample.vpc_stack import VpcStack

app = cdk.App()
LambdaStack(app, "LambdaStack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))  # env={'region': 'us-east-1'})

VPC = VpcStack(app, "VpcStack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))

EcsStack(app, "EcsStack", vpc=VPC.vpc, env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))


app.synth()
