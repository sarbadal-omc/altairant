from file_manager.gcs_file_system import GCSFileSystem
from google.oauth2 import service_account


class TestGCSFileSystem:
    JSON_KEY = ("/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/"
               "development-490607-06eae129a3e2.json")
    CREDS = service_account.Credentials.from_service_account_file(JSON_KEY)

    def setup(self):
        self.gcs_path = "gs://open-file-testing/test_file_gcs.txt"
        self.write_to_path = "gs://open-file-testing/test_write_fileSystem.txt"
        self.gcs_fs = GCSFileSystem(credentials=self.CREDS)

    def test_read_from_gcs(self):
        with self.gcs_fs.open(self.gcs_path, mode="r") as f:
            content = f.read()
            print(content)
            assert len(content) > 0  # Basic check to ensure we read something

    def test_write_to_gcs(self):
        test_content = "Hello, GCS! This is a test write."
        with self.gcs_fs.open(self.write_to_path, mode="w") as f:
            f.write(test_content)

    def test_verify_written_content(self):
        with self.gcs_fs.open(self.write_to_path, mode="r") as f:
            content = f.read()
            print(content)
            assert content == "Hello, GCS! This is a test write."

    def cleanup(self):
        # Cleanup test file from GCS --- IGNORE ---
        client = self.gcs_fs.client
        bucket_name, blob_name = self.write_to_path.split("gs://", 1)[1].split("/", 1)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()

def main():
    test_gcs_fs = TestGCSFileSystem()
    test_gcs_fs.setup()
    test_gcs_fs.test_read_from_gcs()
    test_gcs_fs.test_write_to_gcs()
    test_gcs_fs.test_verify_written_content()
    test_gcs_fs.cleanup()


if __name__ == "__main__":
    main()