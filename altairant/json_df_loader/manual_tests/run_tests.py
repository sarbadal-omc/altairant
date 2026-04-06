import json
import os

from altairant.json_df_loader import JsonToDataFrameLoader
 

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
 
 
def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r") as f:
        return json.load(f)
 
 
def print_result(test_name, success, error=None):
    if success:
        print(f"[PASS] {test_name}")
    else:
        print(f"[FAIL] {test_name}")
        if error:
            print(f"       Error: {error}")
 
 
def test_list_of_dicts(loader):
    try:
        data = load_json("list_of_dicts.json")
        df = loader.load(data)
 
        assert list(df.columns) == ["name", "age", "city"]
        assert len(df) == 5
        assert df.iloc[0]["name"] == "Alice"

        # print(df.head())
        print_result("ListOfDicts", True)
    except Exception as e:
        print_result("ListOfDicts", False, e)
 
 
def test_nested_data(loader):
    try:
        data = load_json("nested_data.json")
        df = loader.load(data)
 
        assert list(df.columns) == ["id", "name", "age", "city"]
        assert len(df) == 5

        # print(df.head())
        print_result("NestedData", True)
    except Exception as e:
        print_result("NestedData", False, e)
 
 
def test_columnar(loader):
    try:
        data = load_json("columnar.json")
        df = loader.load(data)
 
        assert list(df.columns) == ["name", "age", "city"]
        assert df.iloc[1]["name"] == "Bob"
 
        # print(df.head())
        print_result("Columnar", True)
    except Exception as e:
        print_result("Columnar", False, e)
 
 
def test_column_rows(loader):
    try:
        data = load_json("column_rows.json")
        df = loader.load(data)
 
        assert list(df.columns) == ["id", "name", "age", "city", "score"]
        assert len(df) == 5
        assert df.iloc[2]["name"] == "Charlie"
 
        print(df.head())
        print_result("ColumnRows", True)
    except Exception as e:
        print_result("ColumnRows", False, e)
 
 
def test_invalid_schema(loader):
    try:
        data = {"invalid": "format"}
        loader.load(data)
        print_result("InvalidSchema", False, "Expected failure but passed")
    except Exception:
        print_result("InvalidSchema", True)
 
 
def run_all_tests():
    loader = JsonToDataFrameLoader()
 
    print("\nRunning Manual Tests...\n")
 
    test_list_of_dicts(loader)
    test_nested_data(loader)
    test_columnar(loader)
    test_column_rows(loader)
    test_invalid_schema(loader)
 
    print("\nDone.\n")
 
 
if __name__ == "__main__":
    run_all_tests()
 