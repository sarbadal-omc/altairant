import os
import tempfile
import duckdb
from google.oauth2 import service_account

from duckstore.duckstore import (
    parse_uri,
    LocalBackend,
    GCSBackend,
    DuckDBCloud,
)


class TestDuckDBCloud:
    JSON_KEY = ("/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/Documents/"
               "development-490607-06eae129a3e2.json")
    CREDS = service_account.Credentials.from_service_account_file(JSON_KEY)
    URI = "gs://open-file-testing/demo.duckdb"
    # LOCAL_URI = "file:///tmp/test.duckdb"

    def test_one_shot_execution(self):

        def test_execute(self):
            print("Testing one-shot execution...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
            db.execute("CREATE TABLE IF NOT EXISTS test AS SELECT 1 AS id, 'foo' AS name")
            db.execute("INSERT INTO test VALUES (2, 'bar')")
            results = db.execute("SELECT * FROM test")
            assert results == [(1, 'foo'), (2, 'bar')]

        def test_query_df(self):
            print("Testing one-shot query_df...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
            df = db.query_df("SELECT * FROM test")
            assert list(df.columns) == ['id', 'name']
            assert len(df) == 2
            assert df.iloc[0]['id'] == 1
            assert df.iloc[0]['name'] == 'foo'
            assert df.iloc[1]['id'] == 2
            assert df.iloc[1]['name'] == 'bar'

        def test_persisted_data_in_db(self):
            print("Testing persisted data in DB...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
            results = db.execute("SELECT * FROM test")
            assert results == [(1, 'foo'), (2, 'bar')]

        def test_list_tables(self):
            print("Testing list_tables...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
            tables = db.list_tables()
            assert ('test',) in tables

        test_execute(self)
        test_query_df(self)
        test_persisted_data_in_db(self)
        test_list_tables(self)


    def test_session_usage(self):

        def test_session_execution(self):
            print("Testing session execution...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
            with db.session() as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS session_test AS SELECT 3 AS id, 'baz' AS name")
                conn.execute("INSERT INTO session_test VALUES (4, 'qux')")
                results = conn.execute("SELECT * FROM session_test").fetchall()
                assert results == [(3, 'baz'), (4, 'qux')]

        def test_session_query_df(self):
            print("Testing session query_df...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
            with db.session() as conn:
                df = conn.execute("SELECT * FROM session_test").df()
                assert list(df.columns) == ['id', 'name']
                assert len(df) == 2
                assert df.iloc[0]['id'] == 3
                assert df.iloc[0]['name'] == 'baz'
                assert df.iloc[1]['id'] == 4
                assert df.iloc[1]['name'] == 'qux'

        def test_session_isolation(self):
            print("Testing session isolation...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
            with db.session() as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS isolation_test AS SELECT 5 AS id, 'quux' AS name")
                conn.execute("INSERT INTO isolation_test VALUES (6, 'corge')")
                results = conn.execute("SELECT * FROM isolation_test").fetchall()
                assert results == [(5, 'quux'), (6, 'corge')]

            # New session should see the same data
            with db.session() as conn:
                results = conn.execute("SELECT * FROM isolation_test").fetchall()
                assert results == [(5, 'quux'), (6, 'corge')]

        test_session_execution(self)
        test_session_query_df(self)
        test_session_isolation(self)


    def test_read_only_mode(self):

        def test_read_only_execution(self):
            print("Testing read-only execution...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=True)
            with db.session() as conn:
                results = conn.execute("SELECT * FROM test").fetchall()
                assert results == [(1, 'foo'), (2, 'bar')]
                try:
                    conn.execute("INSERT INTO test VALUES (3, 'baz')")
                    assert False, "Expected exception on write in read-only mode"
                except Exception as e:
                    assert "read-only" in str(e).lower()

        def test_read_only_query_df(self):
            print("Testing read-only query_df...")
            db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=True)
            with db.session() as conn:
                df = conn.execute("SELECT * FROM test").df()
                assert list(df.columns) == ['id', 'name']
                assert len(df) == 2
                assert df.iloc[0]['id'] == 1
                assert df.iloc[0]['name'] == 'foo'
                assert df.iloc[1]['id'] == 2
                assert df.iloc[1]['name'] == 'bar'
                try:
                    conn.execute("INSERT INTO test VALUES (3, 'baz')")
                    assert False, "Expected exception on write in read-only mode"
                except Exception as e:
                    assert "read-only" in str(e).lower()

    def test_local_file_usage(self):

        def test_local_file_execution(self):
            print("Testing local file execution...")
            with tempfile.NamedTemporaryFile(suffix=".duckdb") as tmp:
                local_uri = tmp.name
                db = DuckDBCloud(local_uri, read_only=False)
                db.execute("CREATE TABLE IF NOT EXISTS local_test AS SELECT 42 AS answer")
                results = db.execute("SELECT * FROM local_test")
                assert results == [(42,)]

        def test_local_file_query_df(self):
            print("Testing local file query_df...")
            with tempfile.NamedTemporaryFile(suffix=".duckdb") as tmp:
                local_uri = tmp.name
                db = DuckDBCloud(local_uri, read_only=False)
                db.execute("CREATE TABLE IF NOT EXISTS local_test AS SELECT 42 AS answer")
                df = db.query_df("SELECT * FROM local_test")
                assert list(df.columns) == ['answer']
                assert len(df) == 1
                assert df.iloc[0]['answer'] == 42

    def cleanup(self):
        print("Cleaning up test tables...")
        db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
        with db.session() as conn:
            conn.execute("DROP TABLE IF EXISTS test")
            conn.execute("DROP TABLE IF EXISTS session_test")
            conn.execute("DROP TABLE IF EXISTS isolation_test")

        db = DuckDBCloud(self.URI, credentials=self.CREDS, read_only=False)
        with db.session() as conn:
            print("Remaining tables after cleanup:", conn.execute("SHOW TABLES").fetchall())
            assert ('test',) not in conn.execute("SHOW TABLES").fetchall()
            assert ('session_test',) not in conn.execute("SHOW TABLES").fetchall()
            assert ('isolation_test',) not in conn.execute("SHOW TABLES").fetchall()
            conn.execute("SHOW TABLES")


def main():
    # Run tests
    test_duckdb = TestDuckDBCloud()
    test_duckdb.test_one_shot_execution()
    test_duckdb.test_session_usage()
    test_duckdb.test_read_only_mode()
    test_duckdb.test_local_file_usage()
    test_duckdb.cleanup()
    print("All tests passed!")


if __name__ == "__main__":
    main()
