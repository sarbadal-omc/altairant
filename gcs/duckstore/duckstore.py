import duckdb
import tempfile
import os
import shutil
from contextlib import contextmanager
from urllib.parse import urlparse
 
from google.cloud import storage
 

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
    def __init__(self, bucket: str, blob_path: str, credentials: storage.credentials.Credentials = None):
        if credentials:
            self.client = storage.Client(credentials=credentials)
        else:
            self.client = storage.Client()
 
        self.bucket = self.client.bucket(bucket)
        self.blob = self.bucket.blob(blob_path)
 
    def download(self, local_path: str) -> None:
        if self.blob.exists():
            self.blob.download_to_filename(local_path)
        
        # Always ensure valid DuckDB file exists
        conn = duckdb.connect(local_path)
        conn.close()
 
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

    if scheme == "gs":
        scheme = "gcs"
 
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
    def __init__(self, uri: str, credentials: storage.credentials.Credentials = None, read_only: bool = False, local_path: str = None):
        self.uri = uri
        self.credentials = credentials
        self.read_only = read_only
        self.local_override_path = local_path
 
        scheme, bucket, path = parse_uri(uri)
 
        if scheme == "gcs":
            self.backend = GCSBackend(bucket, path, credentials)
        elif scheme == "s3":
            self.backend = S3Backend(bucket, path)
        elif scheme == "file":
            self.backend = LocalBackend(path)
        else:
            raise ValueError(f"Unsupported scheme: {scheme}")

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
 
        if not os.path.exists(self._local_path) or os.path.getsize(self._local_path) == 0:
            print("Creating fresh DuckDB file at local path.")
            conn = duckdb.connect(self._local_path)
            conn.execute("CREATE TABLE IF NOT EXISTS __init (id INTEGER)")
            conn.close()
        
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
    def connect(self):
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

