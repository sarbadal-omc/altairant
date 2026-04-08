"""
This module defines the BaseSchemaHandler class, which serves as an abstract 
base class for handling different JSON schemas and converting them into 
pandas DataFrames. It provides a registry mechanism to manage multiple handlers 
and ensures that each handler implements the necessary methods for schema 
validation and DataFrame conversion.
"""
import pandas as pd
from abc import ABC, abstractmethod
 
 
class BaseSchemaHandler(ABC):
    _registry = []
 
    @classmethod
    def register(cls, handler):
        """Register a new handler instance. The handler must be an instance of BaseSchemaHandler."""
        if not isinstance(handler, BaseSchemaHandler):
            raise TypeError("Handler must be an instance of BaseSchemaHandler")
        cls._registry.append(handler)
 
    @classmethod
    def clear_registry(cls):
        """Clear all registered handlers. Useful for testing or resetting state."""
        cls._registry = []
 
    @classmethod
    def get_all_handlers(cls):
        """Return a list of all registered handler instances."""
        return cls._registry
 
    @abstractmethod
    def can_handle(self, data: dict | list) -> bool:
        """Determine if this handler can process the given data."""
        pass
 
    @abstractmethod
    def to_dataframe(self, data: dict | list, **context) -> pd.DataFrame:
        """Convert the input data to a pandas DataFrame. The context can include
        additional dependencies or configuration needed for processing."""
        pass

    @abstractmethod
    def schema_name(self) -> str:
        """Human-readable name for the schema this handler processes."""
        pass

    @abstractmethod
    def description(self) -> str:
        """Brief description of the schema and its intended use case."""
        pass

    @abstractmethod
    def example(self) -> dict | list:
        """A small example of data that conforms to this schema."""
        pass