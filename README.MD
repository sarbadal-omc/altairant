# AltairAnt

A small Python project to work with Google Cloud Storage and DuckDB.

## Overview

This repository contains utilities for accessing GCS files and integrating with DuckDB.

## Requirements

- Python 3
- `google-cloud-storage`
- `duckdb`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Update the `JSON_KEY` path in `main.py` with your GCS service account key file and implement the `main()` logic as needed.

Run the main script:

```bash
python main.py
```

## Tests

There are test files under `gcs/` for the GCS file system and DuckDB integration.

```bash
python -m pytest
```
