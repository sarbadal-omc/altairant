import pandas as pd
from .base_handler import BaseSchemaHandler


class ListOfDictsHandler(BaseSchemaHandler):
    def can_handle(self, data):
        return isinstance(data, list) and all(isinstance(x, dict) for x in data)
 
    def to_dataframe(self, data):
        return pd.DataFrame(data)