import json
import sys

from processor import process_file

CSV_DATA = """contractor_name,payment_date,payment_amount,cumulative_ytd,w9_status,tin_match_status
Acme Plumbing,2024-03-15,750.00,750.00,valid,valid
Bright Electric LLC,2024-03-20,450.00,550.00,awaiting signature,
Summit Roofing,2024-02-10,300.00,300.00,,
"""


def main():
    records = process_file(CSV_DATA.encode("utf-8"))

    assert isinstance(records, list), "Expected list result"
    assert len(records) == 3, f"Expected 3 records, got {len(records)}"

    titles = [r["title"] for r in records]
    assert "Acme Plumbing" in titles, f"Missing Acme Plumbing: {titles}"
    assert "Bright Electric LLC" in titles, f"Missing Bright Electric LLC: {titles}"
    assert "Summit Roofing" in titles, f"Missing Summit Roofing: {titles}"

    for record in records:
        assert "title" in record, "Record missing title"
        assert "status" in record, "Record missing status"
        assert "details" in record, "Record missing details"
        assert "due_date" in record, "Record missing due_date"
        assert isinstance(record["details"], dict), "details must be a dict"

    print(json.dumps(records, indent=2))
    print("DEMO OK: 3 records, list shape and titles verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
