# from gcs import GCSFileSystem
from google.oauth2 import service_account

from altairant.gcs.duckstore.duckstore import DuckDBCloud

JSON_KEY = "/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/development-490607-06eae129a3e2.json"
creds = service_account.Credentials.from_service_account_file(JSON_KEY)


def main(): 
    bucket = "open-file-testing"
    blob_path = "demo.duckdb"
    db = DuckDBCloud(f"gs://{bucket}/{blob_path}", credentials=creds)
    
    db.execute("CREATE TABLE IF NOT EXISTS test AS SELECT 1 AS id, 'foo' AS name")
    print(db.execute("SELECT * FROM test"))


if __name__ == "__main__":
    main()