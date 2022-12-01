import aws_cdk as cdk
from constructs import Construct


class Database(Construct):
    def __init__(self, scope: Construct, id_: str):
        super().__init__(scope, id_)
