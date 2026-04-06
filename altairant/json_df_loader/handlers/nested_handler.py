import pandas as pd
from .base_handler import BaseSchemaHandler


class NestedDataKeyHandler(BaseSchemaHandler):
    def can_handle(self, data):
        return isinstance(data, dict) and "data" in data
 
    def to_dataframe(self, data):
        return pd.json_normalize(data["data"])