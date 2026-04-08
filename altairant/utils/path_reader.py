"""
This module provides a utility function to read content from a given path, which 
can be either a local file path or a Google Cloud Storage (GCS) path. 
The function uses the appropriate method to read the content based on the path type.
"""
from google.auth.credentials import Credentials
from altairant.gcs.file_manager.gcs_file_system import GCSFileSystem


def read_path(path: str, credentials: Credentials = None) -> str:
    if path.startswith("gs://"):
        gcs_fs = GCSFileSystem(credentials=credentials)
        with gcs_fs.open(path, mode="r") as f:
            content = f.read()
        return content

    with open(path, mode="r", encoding="utf-8") as f:
        return f.read()