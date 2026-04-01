from gcs import GCSFileSystem
from google.oauth2 import service_account

JSON_KEY = "/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/development-490607-06eae129a3e2.json"
creds = service_account.Credentials.from_service_account_file(JSON_KEY)


def main():
    
    # Example usage
    gcs_path = "gs://open-file-testing/sftp_logins.json"
    write_to_path = "gs://open-file-testing/test_write_fileSystem2.txt"
    gcs_fs = GCSFileSystem(credentials=creds)
    
    # Writing to GCS
    with gcs_fs.open(write_to_path, mode="w") as f:
        f.write("Hello, GCS!")
    
    # Reading from GCS
    with gcs_fs.open(gcs_path, mode="r") as f:
        content = f.read()
        print(content)


if __name__ == "__main__":
    main()