"""
This module defines a handler for the "column-rows" schema, which represents a 
DataFrame as a dictionary with "columns" and "rows" keys. The "columns"
key contains metadata about the columns (name and dtype), while the "rows" key
contains the actual data as a list of lists. This handler can convert such a
structure into a pandas DataFrame, applying appropriate data types based on the provided metadata.

Example input:
{
    "columns": [
        {"name": "id", "dtype": "int64"},
        {"name": "name", "dtype": "string"},
        {"name": "value", "dtype": "float64"}
    ],
    "rows": [
        [1, "foo", 3.14],
        [2, "bar", 2.71]
    ]
}
"""
import pandas as pd
from .base_handler import BaseSchemaHandler
 
 
class ColumnRowsHandler(BaseSchemaHandler):
    def can_handle(self, data):
        return (
            isinstance(data, dict)
            and "columns" in data
            and "rows" in data
            and isinstance(data["columns"], list)
            and isinstance(data["rows"], list)
        )
 
    def to_dataframe(self, data):
        columns_meta = data["columns"]
        rows = data["rows"]
 
        # Extract column names
        column_names = [col["name"] for col in columns_meta]
        df = pd.DataFrame(rows, columns=column_names)

 
        dtype_mapping = {
            "int64": "Int64",
            "float64": "float64",
            "string": "string",
            "bool": "boolean"
        }
 
        for col in columns_meta:
            col_name = col["name"]
            dtype = col.get("dtype")
 
            if dtype in dtype_mapping:
                try:
                    df[col_name] = df[col_name].astype(dtype_mapping[dtype])
                except Exception:
                    # Fail silently if conversion fails
                    pass
 
        return df

    def schema_name(self) -> str:
        return "Column-Rows Format"

    def description(self) -> str:
        return "A format where data is represented as a dictionary with 'columns' metadata and 'rows' data."

    def example(self) -> dict:
        return {
            "columns": [
                {"name": "id", "dtype": "int64"},
                {"name": "name", "dtype": "string"},
                {"name": "value", "dtype": "float64"}
            ],
            "rows": [
                [1, "foo", 3.14],
                [2, "bar", 2.71]
            ]
        }