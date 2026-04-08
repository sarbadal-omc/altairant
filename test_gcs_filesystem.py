from google.oauth2 import service_account
from altairant.gcs import GCSFileSystem


JSON_KEY = "/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/" \
           "development-490607-06eae129a3e2.json"  # Update with your actual path to the service account JSON key
CREDS = service_account.Credentials.from_service_account_file(JSON_KEY)


def print_result(test_name, success, error=None):
    if success:
        print(f"{test_name} test passed.")
    else:
        print(f"{test_name} test failed. Error: {error}")


def test_gcs_file_system():
    try:
        write_to_file_path = "gs://open-file-testing/test_write_filesystem.txt"  # Update with your actual GCS path

        # Initialize GCSFileSystem with credentials
        gcs_fs = GCSFileSystem(credentials=CREDS)
        
        # Writing to GCS
        with gcs_fs.open(write_to_file_path, mode="w") as f:
            f.write("This is a test file for testing gcs.file_manager module.")
        
        # Reading from GCS
        with gcs_fs.open(write_to_file_path, mode="r") as f:
            content = f.read()
            assert content == "This is a test file for testing gcs.file_manager module."

        print_result("GCSFileSystem", True)
    except Exception as e:
        print_result("GCSFileSystem", False, e)


def run_all_tests():
    test_gcs_file_system()


if __name__ == "__main__":
    run_all_tests()