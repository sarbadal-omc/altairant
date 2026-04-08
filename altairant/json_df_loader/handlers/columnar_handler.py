"""
This module defines a ColumnarHandler class that can handle columnar data formats, 
where the data is represented as a dictionary of column names to lists of values. 
The handler checks if the input data is a dictionary where all values are lists, 
and if so, it converts it into a pandas DataFrame. This format is common in various 
data interchange formats and can be easily converted to a DataFrame for further analysis.

Example input:
{
    "id": [1, 2, 3],
    "name": ["foo", "bar", "baz"],
    "value": [3.14, 2.71, 1.62]
}
"""
import pandas as pd
from .base_handler import BaseSchemaHandler


class ColumnarHandler(BaseSchemaHandler):
    def can_handle(self, data):
        return isinstance(data, dict) and all(isinstance(v, list) for v in data.values())
 
    def to_dataframe(self, data: dict, **context) -> pd.DataFrame:
        return pd.DataFrame(data)

    def schema_name(self) -> str:
        return "Columnar Format"

    def description(self) -> str:
        return "A format where data is represented as a dictionary of column names to lists of values."

    def example(self) -> dict:
        return {
            "id": [1, 2, 3],
            "name": ["foo", "bar", "baz"],
            "value": [3.14, 2.71, 1.62]
        }