"""
update_romance_catalogue.py

1. Pulls romance-ish books from the Open Library Search API.
2. Writes a date-stamped raw CSV, e.g.:
   data/romance_catalogue_250110.csv
3. Merges new rows into data/romance_catalogue.csv (master), de-duplicating by 'link'.

Master file can have extra columns (spice_level, tropes, etc.) which will be preserved.
New rows will have those extra fields blank for you to fill later.
"""

import csv
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

import requests
import pandas as pd


# ------------------- CONFIG -------------------

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TARGET_COUNT = 2000  # adjust as you like
BASE_URL = "https://openlibrary.org/search.json"

ROMANCE_SUBJECTS = [
    "romance",
    "romantic fiction",
    "love stories",
]


def make_raw_output_path() -> Path:
    """Generate a yymmdd-stamped filename."""
    stamp = datetime.utcnow().strftime("%y%m%d")
    return DATA_DIR / f"romance_catalogue_{stamp}.csv"


MASTER_PATH = DATA_DIR / "romance_catalogue.csv"


# ------------------- FETCH HELPERS -------------------

def fetch_page(page: int, limit: int = 100) -> Dict[str, Any]:
    params = {"q": "romance", "page": page, "limit": limit}
    resp = requests.get(BASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def is_romance_doc(doc: Dict[str, Any]) -> bool:
    subjects = doc.get("subject", []) or []
    lower_subjects = " ".join(subjects).lower()
    return any(sub in lower_subjects for sub in ROMANCE_SUBJECTS)


def get_cover_url(doc: Dict[str, Any]) -> str:
    cover_id = doc.get("cover_i")
    if cover_id:
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    return ""


def get_series_info(doc: Dict[str, Any]) -> (str, Optional[int]):
    series = doc.get("series")
    if isinstance(series, list) and series:
        name = series[0]
    else:
        name = series or ""
    series_order = None
    return name, series_order


def extract_description(work_key: str) -> str:
    if not work_key:
        return ""
    try:
        url = f"https://openlibrary.org{work_key}.json"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        desc = data.get("description")
        if isinstance(desc, dict):
            return desc.get("value", "")
        elif isinstance(desc, str):
            return desc
    except Exception:
        return ""
    return ""


def doc_to_row(doc: Dict[str, Any], row_id: int) -> Dict[str, Any]:
    title = doc.get("title", "").strip()
    authors = doc.get("author_name", []) or []
    author = ", ".join(authors[:2])

    series_name, series_order = get_series_info(doc)
    year = doc.get("first_publish_year")
    work_key = doc.get("key")
    link = f"https://openlibrary.org{work_key}" if work_key else ""
    cover_url = get_cover_url(doc)
    description = extract_description(work_key) if work_key else ""

    return {
        "id": row_id,
        "title": title,
        "author": author,
        "series_name": series_name,
        "series_order": series_order if series_order is not None else "",
        "year": year if year is not None else "",
        "description": description.replace("\n", " ").strip(),
        "link": link,
        "cover_url": cover_url,
    }


def write_raw_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    fieldnames = [
        "id",
        "title",
        "author",
        "series_name",
        "series_order",
        "year",
        "description",
        "link",
        "cover_url",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# ------------------- MERGE INTO MASTER -------------------

def merge_into_master(raw_path: Path, master_path: Path) -> None:
    """
    Merge raw data into master catalogue.
    - Uses 'link' as a unique key.
    - Preserves existing rows & columns.
    - Only appends NEW links.
    """
    print(f"Merging {raw_path.name} into {master_path.name}...")

    df_raw = pd.read_csv(raw_path)

    # Ensure basic columns exist
    required_cols = [
        "id", "title", "author", "series_name",
        "series_order", "year", "description", "link", "cover_url",
    ]
    for col in required_cols:
        if col not in df_raw.columns:
            df_raw[col] = ""

    if master_path.exists():
        df_master = pd.read_csv(master_path)
    else:
        # Start fresh master with just the raw columns
        df_master = pd.DataFrame(columns=required_cols)

    # Use 'link' as unique key
    df_master_links = set(df_master["link"].dropna().tolist())
    df_raw_new = df_raw[~df_raw["link"].isin(df_master_links)].copy()

    if df_raw_new.empty:
        print("No new books to add to master.")
        return

    # Align columns: master may have extra cols (spice_level, tropes, etc.)
    for col in df_master.columns:
        if col not in df_raw_new.columns:
            df_raw_new[col] = ""

    # Ensure raw columns exist in master (if new technical fields ever added)
    for col in df_raw_new.columns:
        if col not in df_master.columns:
            df_master[col] = ""

    # Reorder columns to master order, then append new rows
    df_raw_new = df_raw_new[df_master.columns]
    df_updated = pd.concat([df_master, df_raw_new], ignore_index=True)

    df_updated.to_csv(master_path, index=False, encoding="utf-8")
    print(f"Added {len(df_raw_new)} new books to {master_path.name}")


# ------------------- MAIN -------------------

def main():
    all_rows: List[Dict[str, Any]] = []
    page = 1
    row_id = 1

    raw_output_path = make_raw_output_path()
    print(f"Fetching romance books… target ~{TARGET_COUNT} rows")
    print(f"Raw output: {raw_output_path}")

    while len(all_rows) < TARGET_COUNT:
        print(f"Fetching page {page}...")
        try:
            data = fetch_page(page=page, limit=100)
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

        docs = data.get("docs", [])
        if not docs:
            print("No more docs returned, stopping.")
            break

        for doc in docs:
            if not is_romance_doc(doc):
                continue

            row = doc_to_row(doc, row_id=row_id)
            if not row["title"] or not row["author"]:
                continue

            all_rows.append(row)
            row_id += 1

            if len(all_rows) >= TARGET_COUNT:
                break

        page += 1
        time.sleep(1.0)

    print(f"Collected {len(all_rows)} romance-ish books.")
    write_raw_csv(all_rows, raw_output_path)
    print(f"Wrote {len(all_rows)} rows to {raw_output_path.resolve()}")

    # Merge into master
    merge_into_master(raw_output_path, MASTER_PATH)


if __name__ == "__main__":
    main()
