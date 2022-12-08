from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from constructs import Construct

from backend.api.infrastructure import API
from backend.database.infrastructure import Database


class Backend(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        database_dynamodb_billing_mode: dynamodb.BillingMode,
        api_lambda_reserved_concurrency: int,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        database = Database(
            self,
            "Database",
            dynamodb_billing_mode=database_dynamodb_billing_mode,
        )
        api = API(
            self,
            "API",
            users_dynamodb_table_name=database.users_dynamodb_table.table_name,
            orders_dynamodb_table_name=database.orders_dynamodb_table.table_name,
            lambda_reserved_concurrency=api_lambda_reserved_concurrency,
        )

        database.users_dynamodb_table.grant_read_write_data(api.users_lambda_function)
        database.orders_dynamodb_table.grant_read_write_data(api.orders_lambda_function)

        self.api_endpoint = cdk.CfnOutput(
            self,
            "APIEndpoint",
            value=api.api_gateway_http_api.url,
        )
