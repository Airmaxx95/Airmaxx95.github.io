#!/usr/bin/env python3
import csv
import io
import json
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 csv_to_site_items_json.py data/site_items.csv [data/site_items.json]")
        return 1

    csv_path = Path(sys.argv[1])
    json_path = Path(sys.argv[2]) if len(sys.argv) > 2 else csv_path.with_suffix(".json")

    text = csv_path.read_text(encoding="latin1")
    rows = list(csv.reader(io.StringIO(text)))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and str(row[0]).strip() == "ASN")
    except StopIteration:
        raise SystemExit("Could not find CSV header row beginning with ASN.")

    headers = rows[header_index]
    body_rows = [row for row in rows[header_index + 1:] if any(str(cell).strip() for cell in row)]

    records = []
    for row in body_rows:
        record = {}
        for i, header in enumerate(headers):
            record[header] = row[i] if i < len(row) else ""
        records.append(record)

    json_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {json_path} with {len(records)} record(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
