from google.oauth2 import service_account
from altairant.json_df_loader import JsonToDataFrameLoader

json_file = "altairant/json_df_loader/manual_tests/data/columnar.json"

json_key = "/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/" \
           "development-490607-06eae129a3e2.json"
gcs_credentials = service_account.Credentials.from_service_account_file(json_key)

def main():
    loader = JsonToDataFrameLoader(gcs_credentials=gcs_credentials)

    with open(json_file, "r") as f:
        json_input = f.read()

    df = loader.load(json_input)
    print(df.head())

    csv_file = "altairant/json_df_loader/manual_tests/data/csv.json"
    with open(csv_file, "r") as f:
        csv_input = f.read()

    print(loader.load(csv_input))


if __name__ == "__main__":
    main()