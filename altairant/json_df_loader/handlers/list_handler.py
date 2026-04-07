"""
This module defines a ListOfDictsHandler class that can handle data in the 
form of a list of dictionaries and convert it to a pandas DataFrame.

Example input:
[
    {"id": 1, "name": "foo", "value": 3.14},
    {"id": 2, "name": "bar", "value": 2.71}
]
"""
import pandas as pd
from .base_handler import BaseSchemaHandler


class ListOfDictsHandler(BaseSchemaHandler):
    def can_handle(self, data):
        return isinstance(data, list) and all(isinstance(x, dict) for x in data)
 
    def to_dataframe(self, data):
        return pd.DataFrame(data)

    def schema_name(self) -> str:
        return "List of Dicts Format"

    def description(self) -> str:
        return "A format where data is represented as a list of dictionaries, each representing a row of data."

    def example(self) -> list[dict]:
        return [
            {"id": 1, "name": "foo", "value": 3.14},
            {"id": 2, "name": "bar", "value": 2.71}
        ]