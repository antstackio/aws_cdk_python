#!/usr/bin/env python3

import aws_cdk as cdk
import os
from backend.component import Backend


app = cdk.App()
Backend(
    app,
    "sample-app",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)

app.synth()
