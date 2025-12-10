"""
update_openlibrary_romance.py

Fetches romance-ish books from Open Library and writes them to:
  data/romance_openlibrary.csv

Columns:
id, title, author, series_name, series_order, year, description, link, cover_url
"""

import csv
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

import requests

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = DATA_DIR / "romance_openlibrary.csv"

TARGET_COUNT = 2000
BASE_URL = "https://openlibrary.org/search.json"

ROMANCE_SUBJECTS = [
    "romance",
    "romantic fiction",
    "love stories",
]


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


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
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


def main():
    all_rows: List[Dict[str, Any]] = []
    page = 1
    row_id = 1

    print(f"Fetching romance books from Open Library… target ~{TARGET_COUNT} rows")
    print(f"Output: {OUTPUT_PATH}")

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
    write_csv(all_rows, OUTPUT_PATH)
    print(f"Wrote {len(all_rows)} rows to {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
