"""
This module defines a GCSFileSystem class that provides a simple interface for 
reading and writing files to Google Cloud Storage (GCS) using the 
Google Cloud Storage client library.
"""
from contextlib import contextmanager
from google.auth.credentials import Credentials
from google.cloud import storage
import io


class GCSFileSystem:
    def __init__(self, credentials: Credentials = None):
        self.client = storage.Client(credentials=credentials)
 
    @contextmanager
    def open(self, gcs_path, mode="r") -> io.IOBase:
        if not gcs_path.startswith("gs://"):
            raise ValueError("Invalid GCS path")
 
        _, path = gcs_path.split("gs://", 1)
        bucket_name, blob_name = path.split("/", 1)
 
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
 
        if "r" in mode:
            data = blob.download_as_bytes()
            file_obj = io.BytesIO(data) if "b" in mode else io.StringIO(data.decode())
            yield file_obj
            file_obj.close()
 
        elif "w" in mode:
            file_obj = io.BytesIO() if "b" in mode else io.StringIO()
            yield file_obj
            file_obj.seek(0)
 
            if "b" in mode:
                blob.upload_from_file(file_obj)
            else:
                blob.upload_from_string(file_obj.getvalue())
 
            file_obj.close()


def main():
    # Example usage
    from google.oauth2 import service_account
    gcs_path = "gs://open-file-testing/test_file_gcs.txt"
    write_to_path = "gs://open-file-testing/test_write_fileSystem.txt"

    json_key = ("/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/"
               "development-490607-06eae129a3e2.json")
    creds = service_account.Credentials.from_service_account_file(json_key)

    # Initialize GCSFileSystem with credentials
    gcs_fs = GCSFileSystem(credentials=creds)
    
    # Writing to GCS
    with gcs_fs.open(write_to_path, mode="w") as f:
        f.write("Hello, GCS! This is a test write.")

    with open("test_write_fileSystem.txt", "r") as f:
        print(f.read())
    
    # Reading from GCS
    with gcs_fs.open(gcs_path, mode="r") as f:
        content = f.read()
        print(content) 


if __name__ == "__main__":
    main()