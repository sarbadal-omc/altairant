from contextlib import contextmanager
from google.cloud import storage
import io

 
@contextmanager
def gcs_open(gcs_path: str, mode: str = "r", credentials: storage.credentials.Credentials = None) -> io.IOBase:
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