import pathlib

from constructs import Construct


class API(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
    ):
        super().__init__(scope, id_)
