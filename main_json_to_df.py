from altairant.json_df_loader import JsonToDataFrameLoader

json_file = "altairant/json_df_loader/manual_tests/data/columnar.json"

def main():
    loader = JsonToDataFrameLoader()

    with open(json_file, "r") as f:
        json_input = f.read()

    df = loader.load(json_input)
    print(df.head())


if __name__ == "__main__":
    main()