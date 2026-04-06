import pandas as pd
from .base_handler import BaseSchemaHandler


class ColumnarHandler(BaseSchemaHandler):
    def can_handle(self, data):
        return isinstance(data, dict) and all(isinstance(v, list) for v in data.values())
 
    def to_dataframe(self, data):
        return pd.DataFrame(data)
