from altairant.json_df_loader.handlers.inspector import list_available_handlers, print_available_handlers
# from json_df_loader.handlers import list_available_handlers, print_available_handlers
from altairant.json_df_loader import JsonToDataFrameLoader


def main() -> None:
    print_available_handlers(verbose=False)

    # Example usage of JsonToDataFrameLoader with a sample JSON input
    sample_json = {
        "columns": [
            {"name": "id", "dtype": "int64"},
            {"name": "name", "dtype": "string"},
            {"name": "value", "dtype": "float64"}
        ],
        "rows": [
            [1, "foo", 3.14],
            [2, "bar", 2.71]
        ]
    }

    loader = JsonToDataFrameLoader()
    df = loader.load(sample_json)
    print("\nResulting DataFrame:")
    print(df)


if __name__ == "__main__":
    main()