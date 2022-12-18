import aws_cdk as core
import aws_cdk.assertions as assertions
import aws_cdk.aws_dynamodb as dynamodb
from app import Backend


def test_ddb_created():
    app = core.App()
    stack = Backend(
        app,
        "aws-cdk-python",
        api_lambda_reserved_concurrency=1,
        database_dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
    )
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::DynamoDB::Table", {"VisibilityTimeout": 300})


def test_lambda_function_created():
    app = core.App()
    stack = Backend(
        app,
        "aws-cdk-python",
        api_lambda_reserved_concurrency=1,
        database_dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
    )
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::Function", {"VisibilityTimeout": 300}
    )


def test_http_api_created():
    app = core.App()
    stack = Backend(
        app,
        "aws-cdk-python",
        api_lambda_reserved_concurrency=1,
        database_dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
    )
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::ApiGatewayV2::Apie", {"VisibilityTimeout": 300}
    )
