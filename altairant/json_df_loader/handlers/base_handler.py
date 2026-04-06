import pandas as pd
from abc import ABC, abstractmethod
 
 
class BaseSchemaHandler(ABC):
    _registry = []
 
    @classmethod
    def register(cls, handler):
        if not isinstance(handler, BaseSchemaHandler):
            raise TypeError("Handler must be an instance of BaseSchemaHandler")
        cls._registry.append(handler)
 
    @classmethod
    def clear_registry(cls):
        cls._registry = []
 
    @classmethod
    def get_all_handlers(cls):
        return cls._registry
 
    @abstractmethod
    def can_handle(self, data: dict | list) -> bool:
        pass
 
    @abstractmethod
    def to_dataframe(self, data: dict | list) -> pd.DataFrame:
        pass