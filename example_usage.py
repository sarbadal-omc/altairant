from file_manager.gcs_file_system import GCSFileSystem
from google.oauth2 import service_account


JSON_KEY = ("/path/to/service_account.json")  # Update with your actual path to the service account JSON key
CREDS = service_account.Credentials.from_service_account_file(JSON_KEY)


def example_usage_gcs_file_system():
    gcs_path = "gs://open-file-testing/test_file_gcs.txt"  # Update with your actual GCS path
    write_to_path = "gs://open-file-testing/test_write_fileSystem.txt"  # Update with your actual GCS path

    # Initialize GCSFileSystem with credentials
    gcs_fs = GCSFileSystem(credentials=CREDS)
    
    # Writing to GCS
    with gcs_fs.open(write_to_path, mode="w") as f:
        f.write("Hello, GCS! This is a test write.")

    with open("test_write_fileSystem.txt", "r") as f:
        print(f.read())
    
    # Reading from GCS
    with gcs_fs.open(gcs_path, mode="r") as f:
        content = f.read()
        print(content)


def example_usage_cloud_duckstore():
    import os
    import tempfile
    import duckdb
    from google.oauth2 import service_account

    from altairant.gcs.duckstore.duckstore import (
        parse_uri,
        LocalBackend,
        GCSBackend,
        DuckDBCloud,
    )

    db = DuckDBCloud("gs://open-file-testing/demo.duckdb", credentials=CREDS, read_only=False)
    db.execute("CREATE TABLE IF NOT EXISTS test AS SELECT 1 AS id, 'foo' AS name")
    db.execute("INSERT INTO test VALUES (2, 'bar')")
    results = db.execute("SELECT * FROM test")
    print(results)


def main():
    example_usage_gcs_file_system()
    example_usage_cloud_duckstore()


if __name__ == "__main__":
    main()