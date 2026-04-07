"""
This module provides utilities for inspecting and listing available JSON schema 
handlers that can convert JSON data into pandas DataFrames. It includes functions 
to list all registered handlers, print their details in a readable format, and 
find a suitable handler for a given JSON input.
"""
import textwrap
import json
from .base_handler import BaseSchemaHandler
from .registry import register_all_handlers

register_all_handlers()


def list_available_handlers(verbose=False) -> list[dict]:
    """Returns a list of available JSON schema handlers with their 
    names, descriptions, and optionally examples."""
    handlers = BaseSchemaHandler.get_all_handlers()
    print(f"Found {len(handlers)} registered handlers.")

    result = []

    for handler in handlers:
        info = {
            "schema_name": handler.schema_name(),
            "class_name": handler.__class__.__name__,
            "description": handler.description(),
        }

        if verbose:
            info["example"] = handler.example()

        result.append(info)

    return result


def print_available_handlers(verbose=False) -> None:
    """Prints the available JSON schema handlers in a readable format."""
    handlers = list_available_handlers(verbose)

    print("\nAvailable JSON Schema Handlers:\n")

    for handler in handlers:
        print(f"\tName: {handler['schema_name']}")
        print(f"\tClass: {handler['class_name']}")
        print(f"\tDescription: {handler['description']}")

        if verbose:
            example_json = textwrap.indent(f"'''{json.dumps(handler['example'], indent=2)}'''", "\t\t")
            print(f"\tExample:\n{example_json}")

        print("-" * 120)


def find_matching_handler(data) -> BaseSchemaHandler:
    """Finds and returns the first handler that can process the given data."""
    handlers = BaseSchemaHandler.get_all_handlers()

    for handler in handlers:
        if handler.can_handle(data):
            return handler

    raise ValueError("No suitable handler found for the provided data.")