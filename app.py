#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_sample.lambda_stack import LambdaStack

app = cdk.App()
LambdaStack(app, "LambdaStack", env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"],
                                                    region=os.environ["CDK_DEFAULT_REGION"]))  # env={'region': 'us-east-1'})

app.synth()
