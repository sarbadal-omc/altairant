from gcs import GCSFileSystem
from google.oauth2 import service_account

JSON_KEY = "path/to/service_account.json"
creds = service_account.Credentials.from_service_account_file(JSON_KEY)


def main(): ...


if __name__ == "__main__":
    main()