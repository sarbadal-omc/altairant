"""This module defines the registry for schema handlers in the JSON DataFrame Loader."""
from .base_handler import BaseSchemaHandler
from .list_handler import ListOfDictsHandler
from .nested_handler import NestedDataKeyHandler
from .columnar_handler import ColumnarHandler
from .column_rows_handler import ColumnRowsHandler
 
 
def register_all_handlers():
    """Registers all available handlers in the BaseSchemaHandler registry."""
    BaseSchemaHandler.clear_registry()
 
    BaseSchemaHandler.register(ListOfDictsHandler())
    BaseSchemaHandler.register(NestedDataKeyHandler())
    BaseSchemaHandler.register(ColumnRowsHandler())
    BaseSchemaHandler.register(ColumnarHandler())