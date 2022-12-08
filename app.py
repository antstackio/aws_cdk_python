#!/usr/bin/env python3

import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from backend.component import Backend


app = cdk.App()

# Component sandbox stack
Backend(
    app,
    "SampleApp",
    api_lambda_reserved_concurrency=1,
    database_dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
)

app.synth()
