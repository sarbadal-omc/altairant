# AltairAnt

A Python library providing unified utilities for working with local and cloud-based data, including DuckDB database wrappers, file system abstractions for Google Cloud Storage (GCS), and JSON to DataFrame loading with multiple schema handlers.

## Features

- **DuckDB Integration**: Simplified database operations with context-managed connections.
- **GCS File System**: Seamless file access and synchronization between local and remote storage.
- **JSON to DataFrame Loader**: Automatic conversion of various JSON formats to pandas DataFrames using extensible schema handlers.

## Installation

Install from source or via pip:

```bash
pip install altairant
```

## Usage

### JSON to DataFrame Loader

```python
from altairant.json_df_loader import JsonToDataFrameLoader

loader = JsonToDataFrameLoader()

# Example: List of dicts
data = [
    {"id": 1, "name": "Alice", "value": 3.14},
    {"id": 2, "name": "Bob", "value": 2.71}
]

df = loader.load(data)
print(df)
```

Supported JSON schemas include:
- List of dictionaries
- Columnar format (dict of lists)
- Column-rows format (with metadata)
- Nested data under a "data" key

### DuckDB Wrapper

```python
from altairant.gcs.duckstore import DuckDBStore

# Example usage (assuming GCS setup)
```

### GCS File System

```python
from altairant.gcs.file_manager import GCSFileManager

# Example usage
```

## Requirements

- Python >= 3.8
- pandas
- duckdb
- google-cloud-storage
- gcsfs

## License

MIT License