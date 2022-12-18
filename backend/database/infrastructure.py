import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from constructs import Construct


class Database(cdk.NestedStack):
    def __init__(
        self, scope: Construct, id_: str, *, dynamodb_billing_mode: dynamodb.BillingMode
    ):
        super().__init__(scope, id_)

        users_partition_key = dynamodb.Attribute(
            name="username", type=dynamodb.AttributeType.STRING
        )
        orders_partition_key = dynamodb.Attribute(
            name="orderid", type=dynamodb.AttributeType.STRING
        )
        self.users_dynamodb_table = dynamodb.Table(
            self,
            "UsersDynamoDBTable",
            billing_mode=dynamodb_billing_mode,
            partition_key=users_partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        self.orders_dynamodb_table = dynamodb.Table(
            self,
            "OrdersDynamoDBTable",
            billing_mode=dynamodb_billing_mode,
            partition_key=orders_partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
