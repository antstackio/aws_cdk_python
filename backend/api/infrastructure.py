import pathlib

import aws_cdk.aws_apigatewayv2_alpha as apigatewayv2
import aws_cdk.aws_apigatewayv2_integrations_alpha as apigatewayv2_integrations_alpha
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_lambda_python_alpha as lambda_python_alpha
from constructs import Construct
from aws_cdk import App, CfnOutput, NestedStack, NestedStackProps, Stack


class API(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        users_dynamodb_table_name: str,
        orders_dynamodb_table_name: str,
        lambda_reserved_concurrency: int,
    ):
        super().__init__(scope, id_)

        self.api_gateway_http_api = apigatewayv2.HttpApi(
            self, "SampleAPIGatewayHTTPAPI"
        )

        self.users_lambda_function = lambda_python_alpha.PythonFunction(
            self,
            "UsersLambdaFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={"DYNAMODB_TABLE_NAME": users_dynamodb_table_name},
            reserved_concurrent_executions=lambda_reserved_concurrency,
            entry=str(
                pathlib.Path(__file__).parent.joinpath("runtime/users").resolve()
            ),
            index="lambda_function.py",
            handler="lambda_handler",
        )

        self.users_api_gateway_http_lambda_integration = (
            apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                "UsersAPIGatewayHTTPLambdaIntegration",
                handler=self.users_lambda_function,
            )
        )

        self.api_gateway_http_api.add_routes(
            path=r"/users",
            methods=[apigatewayv2.HttpMethod.ANY],
            integration=self.users_api_gateway_http_lambda_integration,
        )

        self.api_gateway_http_api.add_routes(
            path=r"/users/{username}",
            methods=[apigatewayv2.HttpMethod.ANY],
            integration=self.users_api_gateway_http_lambda_integration,
        )

        self.orders_lambda_function = lambda_python_alpha.PythonFunction(
            self,
            "OrdersLambdaFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={"DYNAMODB_TABLE_NAME": orders_dynamodb_table_name},
            reserved_concurrent_executions=lambda_reserved_concurrency,
            entry=str(
                pathlib.Path(__file__).parent.joinpath("runtime/orders").resolve()
            ),
            index="lambda_function.py",
            handler="lambda_handler",
        )

        self.orders_api_gateway_http_lambda_integration = (
            apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                "OrdersAPIGatewayHTTPLambdaIntegration",
                handler=self.orders_lambda_function,
            )
        )

        self.api_gateway_http_api.add_routes(
            path=r"/orders/{orderid}",
            methods=[apigatewayv2.HttpMethod.ANY],
            integration=self.orders_api_gateway_http_lambda_integration,
        )

        self.api_gateway_http_api.add_routes(
            path=r"/orders",
            methods=[apigatewayv2.HttpMethod.ANY],
            integration=self.orders_api_gateway_http_lambda_integration,
        )
