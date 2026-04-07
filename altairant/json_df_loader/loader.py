"""This module defines the JsonToDataFrameLoader class, which is responsible for 
loading JSON data into a DataFrame using registered schema handlers."""
import json
from .handlers.base_handler import BaseSchemaHandler
from .handlers.registry import register_all_handlers
 
 
class JsonToDataFrameLoader:
    def __init__(self):
        # Explicit registration
        register_all_handlers()
 
        self.handlers = BaseSchemaHandler.get_all_handlers()
 
        # Debug (optional)
        # print("Registered handlers:")
        # for h in self.handlers:
        #     print("-", h.__class__.__name__)
 
    def load(self, json_input):
        if isinstance(json_input, str):
            data = json.loads(json_input)
        else:
            data = json_input
 
        for handler in self.handlers:
            if handler.can_handle(data):
                print(f"Using handler: {handler.__class__.__name__}")
                return handler.to_dataframe(data)
 
        raise ValueError("No suitable schema handler found.")