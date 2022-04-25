#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_sample.cdk_sample_stack import CdkSampleStack


app = cdk.App()
CdkSampleStack(app, "cdk-sample")

app.synth()
