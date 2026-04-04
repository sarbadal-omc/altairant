"""
This module provides a DuckDBCloud class that abstracts away the details of 
using DuckDB with a GCS backend. It allows you to interact with a DuckDB database 
stored in GCS as if it were local, handling all the downloading, uploading, and 
session management for you.
"""
import duckdb
import tempfile
import os
import shutil
from contextlib import contextmanager
from urllib.parse import urlparse
 
import gcsfs
from google.cloud import storage

# Assuming this file is located at altairant/gcs/duckstore/duckstore.py, 
# we want to set the project directory to the root of the repository
PROJECT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

 
class BaseStorageBackend:
    def download(self, local_path: str) -> None:
        raise NotImplementedError
 
    def upload(self, local_path: str) -> None:
        raise NotImplementedError


class LocalBackend(BaseStorageBackend):
    def __init__(self, path):
        self.path = path
 
    def download(self, local_path: str) -> None:
        # No-op: we already have local file
        if not os.path.exists(self.path):
            open(self.path, "wb").close()
 
        # Copy to temp if different
        if self.path != local_path:
            shutil.copy(self.path, local_path)
 
    def upload(self, local_path: str) -> None:
        # Copy back to original location
        if self.path != local_path:
            shutil.copy(local_path, self.path)
 

class GCSBackend(BaseStorageBackend):
    def __init__(self, bucket: str, blob_path: str, credentials: "Credentials" = None, template_path: str = None):
        self.client = storage.Client(credentials=credentials) if credentials else storage.Client()
        self.template_path = template_path or os.path.join(PROJECT_DIR, "gcs/duckstore/_temp.duckdb")
        self.bucket = self.client.bucket(bucket)
        self.blob = self.bucket.blob(blob_path)
 
    def _ensure_blob_exists(self) -> None:
        """If blob doesn't exist → upload template DB"""
        if not self.blob.exists():
            if not os.path.exists(self.template_path):
                raise FileNotFoundError(
                    f"Template DB not found at {self.template_path}"
                )
 
            print("GCS blob not found. Uploading template DB...")
 
            self.blob.upload_from_filename(self.template_path)
 
    def download(self, local_path: str) -> None:
        # Step 1: ensure blob exists
        self._ensure_blob_exists()
 
        # Step 2: download
        self.blob.download_to_filename(local_path)

    def upload(self, local_path: str) -> None:
        self.blob.upload_from_filename(local_path)
 
 
class S3Backend(BaseStorageBackend):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("S3 support not implemented yet.")

 
def parse_uri(uri: str) -> tuple[str, str, str]:
    """Parse URI into (scheme, bucket, path)"""
    if "://" not in uri:
        return "file", "", uri  # Local file
    
    parsed = urlparse(uri)
 
    scheme = parsed.scheme
    bucket = parsed.netloc
    path = parsed.path.lstrip("/")
 
    return scheme, bucket, path


class DuckDBConnectionProxy:
    def __init__(self, conn: duckdb.DuckDBPyConnection, parent: "DuckDBCloud"):
        self._conn = conn
        self._parent = parent
 
    def execute(self, query: str, *args, **kwargs):
        self._parent._mark_dirty(query)
        return self._conn.execute(query, *args, **kwargs)
 
    def __getattr__(self, name):
        return getattr(self._conn, name)

 
class DuckDBCloud:
    def __init__(self, uri: str, credentials: "Credentials" = None, read_only: bool = False, local_path: str = None, template_path: str = None):
        self.uri = uri
        self.credentials = credentials
        self.read_only = read_only
        self.local_override_path = local_path
        self.template_path = template_path
        
        scheme, bucket, path = parse_uri(uri)

        if scheme not in ["gs", "s3", "file"]:
            raise ValueError(f"Unsupported URI scheme: {scheme}")
 
        if scheme == "gs":
            self.backend = GCSBackend(bucket, path, credentials)
        if scheme == "s3":
            self.backend = S3Backend(bucket, path)
        if scheme == "file":
            self.backend = LocalBackend(path)

        # Session state
        self._conn = None
        self._local_path = None
        self._dirty = False

    # Session management
    def open(self) -> duckdb.DuckDBPyConnection:
        """Start a session (manual control)."""
        if self._conn:
            return self._conn

        if self.local_override_path:
            self._local_path = self.local_override_path
        else:
            tmp = tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False)
            self._local_path = tmp.name
            tmp.close()
 
        try:
            self.backend.download(self._local_path)
 
        except Exception as e:
            print(f"Error occurred while downloading: {e}")
            raise
        
        self._conn = duckdb.connect(self._local_path)
        return self._conn

    def close(self):
        """Close session and sync if needed."""
        if not self._conn:
            return
 
        self._conn.close()

        if not self.read_only and self._dirty:
            self.backend.upload(self._local_path)
 
        if os.path.exists(self._local_path):
            os.remove(self._local_path)
 
        self._conn = None
        self._local_path = None
        self._dirty = False
 
    @contextmanager
    def session(self) -> duckdb.DuckDBPyConnection:
        """Context-managed session."""
        conn = self.open()
        proxy_conn = DuckDBConnectionProxy(conn, self)
        try:
            yield proxy_conn
        finally:
            self.close()
 
    # -------------------------------
    # Internal helper
    # -------------------------------
 
    def _mark_dirty(self, query: str) -> None:
        """Mark DB dirty if query is not read-only."""
        query = query.strip().casefold()
        if not query.startswith("select") and not query.startswith("show"):
            self._dirty = True
 
    # -------------------------------
    # One-shot mode (no session)
    # -------------------------------
 
    @contextmanager
    def _connect(self):
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False) as tmp:
            local_path = tmp.name
 
        try:
            self.backend.download(local_path)
            conn = duckdb.connect(local_path)
 
            yield conn
 
            conn.close()
 
            if not self.read_only:
                self.backend.upload(local_path)
 
        finally:
            if os.path.exists(local_path):
                os.remove(local_path)

    @contextmanager
    def connect(self):
        """Context manager for one-shot connection."""
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False) as tmp:
            local_path = tmp.name
        
        try:
            self.backend.download(local_path)
            conn = duckdb.connect(local_path)
 
            yield conn
 
            conn.close()
 
            if not self.read_only:
                self.backend.upload(local_path)

        finally:
            if os.path.exists(local_path):
                os.remove(local_path)
 
    def execute(self, query: str) -> list[tuple]:
        self._mark_dirty(query)
        if self._conn:
            return self._conn.execute(query).fetchall()
        else:
            with self.connect() as conn:
                return conn.execute(query).fetchall()
 
    def query_df(self, query: str) -> "pd.DataFrame":
        if self._conn:
            return self._conn.execute(query).df()
        else:
            with self.connect() as conn:
                return conn.execute(query).df()
 
    def create_table(self, query: str) -> list[tuple]:
        return self.execute(query)
 
    def list_tables(self) -> list[tuple]:
        return self.execute("SHOW TABLES")


if __name__ == "__main__":
    print(f"Project directory: {PROJECT_DIR}")