from gcs import gcs_open
from google.oauth2 import service_account

JSON_KEY = "/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/development-490607-06eae129a3e2.json"
creds = service_account.Credentials.from_service_account_file(JSON_KEY)


def main():
    
    # Example usage
    gcs_path = "gs://open-file-testing/sftp_logins.json"
    write_to_path = "gs://open-file-testing/test_write.txt"
    
    # Writing to GCS
    with gcs_open(write_to_path, mode="w", credentials=creds) as f:
        f.write("Hello, GCS!")
    
    # Reading from GCS
    with gcs_open(gcs_path, mode="r", credentials=creds) as f:
        content = f.read()
        print(content)


if __name__ == "__main__":
    main()