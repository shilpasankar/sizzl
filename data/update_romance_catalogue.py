"""
update_romance_catalogue.py

Pulls romance-ish books from the Open Library Search API and writes them
to romance_catalogue_raw.csv with columns:

id, title, author, series_name, series_order, year, description, link, cover_url

Run this weekly to refresh your raw romance catalogue.
"""

import csv
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

import requests


# ------------------- CONFIG -------------------

# Where to write the CSV
OUTPUT_PATH = Path("romance_catalogue_raw.csv")

# How many total records to aim for in one run
TARGET_COUNT = 2000  # you can raise this over time

# Open Library search parameters
BASE_URL = "https://openlibrary.org/search.json"

# Subject filters to bias towards romance
ROMANCE_SUBJECTS = [
    "romance",
    "romantic fiction",
    "love stories",
]


# ------------------- HELPERS -------------------

def fetch_page(page: int, limit: int = 100) -> Dict[str, Any]:
    """
    Fetch one page of Open Library search results, filtered for romance-ish books.
    We use a generic 'romance' search term and then later filter by subjects.
    """
    params = {
        "q": "romance",
        "page": page,
        "limit": limit,
    }
    resp = requests.get(BASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def is_romance_doc(doc: Dict[str, Any]) -> bool:
    """
    Filter docs to keep only those that are likely romance / romantic fiction.
    We use subject fields when available.
    """
    subjects = doc.get("subject", []) or []
    lower_subjects = " ".join(subjects).lower()
    return any(sub in lower_subjects for sub in ROMANCE_SUBJECTS)


def get_cover_url(doc: Dict[str, Any]) -> str:
    cover_id = doc.get("cover_i")
    if cover_id:
        # Open Library cover API
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    return ""


def get_series_info(doc: Dict[str, Any]) -> (str, Optional[int]):
    """
    Tries to extract a series name and order from Open Library fields.
    Open Library is inconsistent here, so we keep it simple.
    """
    series = doc.get("series")
    if isinstance(series, list) and series:
        name = series[0]
    else:
        name = series or ""

    # Some series strings look like "Series Name ; 1" – we won't overcomplicate.
    # Leave series_order empty unless we want to parse it later.
    series_order = None
    return name, series_order


def extract_description(work_key: str) -> str:
    """
    Optionally fetch a more detailed description for a work.
    This requires an extra API call per work, so we keep it light.
    """
    if not work_key:
        return ""

    # Work endpoint: /works/OLxxxxxW.json
    try:
        url = f"https://openlibrary.org{work_key}.json"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        desc = data.get("description")

        if isinstance(desc, dict):
            # Sometimes description is {"type": "/type/text", "value": "..."}
            return desc.get("value", "")
        elif isinstance(desc, str):
            return desc
    except Exception:
        return ""

    return ""


def doc_to_row(doc: Dict[str, Any], row_id: int) -> Dict[str, Any]:
    """
    Convert an Open Library search doc into our CSV row format.
    """
    title = doc.get("title", "").strip()
    authors = doc.get("author_name", []) or []
    author = ", ".join(authors[:2])

    series_name, series_order = get_series_info(doc)

    year = doc.get("first_publish_year")
    work_key = doc.get("key")  # e.g. /works/OLxxxxxW
    link = f"https://openlibrary.org{work_key}" if work_key else ""

    cover_url = get_cover_url(doc)

    # Optional extra fetch for description (can be commented out to go faster)
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
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# ------------------- MAIN -------------------

def main():
    all_rows: List[Dict[str, Any]] = []
    page = 1
    row_id = 1

    print(f"Fetching romance books from Open Library until we have ~{TARGET_COUNT} records...")

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
            # Skip entries missing a title or author (usually junk)
            if not row["title"] or not row["author"]:
                continue

            all_rows.append(row)
            row_id += 1

            if len(all_rows) >= TARGET_COUNT:
                break

        page += 1
        # Be nice to the API
        time.sleep(1.0)

    print(f"Collected {len(all_rows)} romance-ish books.")
    write_csv(all_rows, OUTPUT_PATH)
    print(f"Wrote {len(all_rows)} rows to {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
