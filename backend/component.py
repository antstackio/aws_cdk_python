from typing import Any

import aws_cdk as cdk
from constructs import Construct

from backend.api.infrastructure import API
from backend.database.infrastructure import Database


class Backend(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        database = Database(self, "Database")
        api = API(self, "API")
