"""
This module defines a NestedDataKeyHandler class that can handle data in a 
nested dictionary format where the actual data is stored under a "data" key. 
The handler converts this nested structure into a pandas DataFrame.

Example input:
{
    "data": [
        {"id": 1, "name": "foo", "value": 3.14},
        {"id": 2, "name": "bar", "value": 2.71}
    ]
}
"""
import pandas as pd
from .base_handler import BaseSchemaHandler


class NestedDataKeyHandler(BaseSchemaHandler):
    def can_handle(self, data):
        return isinstance(data, dict) and "data" in data
 
    def to_dataframe(self, data, **context) -> pd.DataFrame:
        return pd.json_normalize(data["data"])

    def schema_name(self) -> str:
        return "Nested Data Key Format"

    def description(self) -> str:
        return "A format where the actual data is nested under a 'data' key in the JSON structure."

    def example(self) -> dict:
        return {
            "data": [
                {"id": 1, "name": "foo", "value": 3.14},
                {"id": 2, "name": "bar", "value": 2.71}
            ]
        }