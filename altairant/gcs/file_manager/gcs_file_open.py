"""
This module provides a context manager to open GCS files using the 
Google Cloud Storage client library. It allows you to read and write GCS files 
as if they were local files, abstracting away the complexities of interacting 
with GCS directly.
"""
from contextlib import contextmanager
from google.auth.credentials import Credentials
from google.cloud import storage
import io

 
@contextmanager
def gcs_open(gcs_path: str, mode: str = "r", credentials: Credentials = None) -> io.IOBase:
    """
    Open a GCS file like built-in open()
 
    Args:
        gcs_path: str -> "gs://bucket_name/path/to/file"
        mode: "r", "rb", "w", "wb"
        credentials: optional credentials object
    """
 
    if not gcs_path.startswith("gs://"):
        raise ValueError("Invalid GCS path")
 
    # Parse path
    _, path = gcs_path.split("gs://", 1)
    bucket_name, blob_name = path.split("/", 1)
 
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
 
    # READ MODE
    if "r" in mode:
        data = blob.download_as_bytes()
 
        if "b" in mode:
            file_obj = io.BytesIO(data)
        else:
            file_obj = io.StringIO(data.decode("utf-8"))
 
        yield file_obj
        file_obj.close()
 
    # WRITE MODE
    elif "w" in mode:
        if "b" in mode:
            file_obj = io.BytesIO()
        else:
            file_obj = io.StringIO()
 
        yield file_obj
 
        # Upload on close
        file_obj.seek(0)
        if "b" in mode:
            blob.upload_from_file(file_obj)
        else:
            blob.upload_from_string(file_obj.getvalue())
 
        file_obj.close()


def main():
    # Example usage
    from google.oauth2 import service_account
    gcs_path = "gs://open-file-testing/sftp_logins.json"
    write_to_path = "gs://open-file-testing/test_write_gcs_open.txt"

    json_key = ("/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/"
               "development-490607-06eae129a3e2.json")
    creds = service_account.Credentials.from_service_account_file(json_key)

    # Writing to GCS
    with gcs_open(write_to_path, mode="w", credentials=creds) as f:
        f.write("Hello, GCS! This is a test write using gcs_open.")
    
    # Reading from GCS
    with gcs_open(gcs_path, mode="r", credentials=creds) as f:
        content = f.read()
        print(content)


if __name__ == "__main__":
    main()