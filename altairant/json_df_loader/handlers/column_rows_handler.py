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