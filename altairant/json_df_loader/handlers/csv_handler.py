"""
CSVHandler for loading CSV data into a DataFrame. Supports both raw CSV string 
input and file paths (local or GCS).
"""
import pandas as pd
import io
from typing import Any, Dict
 
from .base_handler import BaseSchemaHandler
from altairant.utils.path_reader import read_path
 

class CSVHandler(BaseSchemaHandler):
    def schema_name(self) -> str:
        return "csv"
 
    def description(self) -> str:
        return (
            "Handles CSV input from raw string data or from a path. "
            "Supports local files, GCS paths (gs://), and any source supported by read_path()."
        )

    def example(self) -> Dict[str, Any]:
        return {
            "type": "csv",
            "path": "gs://my-bucket/data/sample.csv",
            "delimiter": ",",
            "read_csv_kwargs": {
                "header": 0
            }
        }

    def can_handle(self, data: list | dict) -> bool:
        return (
            isinstance(data, dict)
            and data.get("type") == "csv"
            and ("data" in data or "path" in data)
        )

    def to_dataframe(self, data: Dict[str, Any], **context) -> pd.DataFrame:
        delimiter = data.get("delimiter", ",")
        read_kwargs = data.get("read_csv_kwargs", {})
 
        if "data" in data:
            csv_content = data["data"]

        elif "path" in data:
            path = data["path"]
            csv_content = read_path(path, credentials=context.get("gcs_credentials"))
 
        else:
            raise ValueError("CSVHandler requires either 'data' or 'path'")

        return pd.read_csv(
            io.StringIO(csv_content),
            sep=delimiter,
            **read_kwargs
        )