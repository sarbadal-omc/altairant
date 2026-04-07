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

# One short execution
JSON_KEY = "path/to/gcp_key.json"
CREDS = service_account.Credentials.from_service_account_file(JSON_KEY)
URI = "gs://your-bucket-name/db.duckdb"

db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
db.execute("CREATE TABLE IF NOT EXISTS test AS SELECT 1 AS id, 'foo' AS name")
results = db.execute("SELECT * FROM test")

# With session
with db.session() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS session_test AS SELECT 3 AS id, 'baz' AS name")
    conn.execute("INSERT INTO session_test VALUES (4, 'qux')")
    results = conn.execute("SELECT * FROM session_test").fetchall()
```

### GCS File System

```python
from google.oauth2 import service_account
from altairant.gcs.file_manager import GCSFileManager

JSON_KEY = "path/to/gcp_key.json"
CREDS = service_account.Credentials.from_service_account_file(JSON_KEY)

gcs_file_path = "gs://your-bucket-name/test_file_gcs.txt"
write_to_file_path = "gs://your-bucket-name/test_write_fileSystem.txt"

gcs_fs = GCSFileSystem(credentials=self.CREDS)
with gcs_fs.open(self.gcs_path, mode="r") as f:
    content = f.read()
    print(content)

test_content = "Hello, GCS! This is a test write."
    with gcs_fs.open(write_to_file_path, mode="w") as f:
        f.write(test_content)

```

## Requirements

- Python >= 3.8
- pandas
- duckdb
- google-cloud-storage
- gcsfs

## License

MIT License