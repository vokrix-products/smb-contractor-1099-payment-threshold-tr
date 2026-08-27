# SMB Contractor 1099 Payment Threshold Tracker & W-9 Chase Automation

Backend processing module for SMB contractor 1099 payment tracking and W-9 chase automation. This repository contains the core file-processing library.

## Archetype

SMB back-office automation: W-9 collection, payment threshold monitoring, and IRS form readiness.

## Product

Parses contractor payment files (CSV, XLSX, PDF, or plain text), normalizes payment and W-9 fields, and derives compliance statuses such as w9_missing:critical, payment_threshold_crossed:info, backup_withholding_risk:critical, and ready_to_file:good.

## Usage

```python
from processor import process_file

with open("payments.csv", "rb") as fh:
    records = process_file(fh.read())
```

Each record has the shape: {"title": str, "status": str, "details": dict, "due_date": str or null}.

## Status values

All allowed statuses are defined in STATUS_VALUES in processor.py.

## Poller input

The poller uploads raw file bytes (PDF, XLSX, CSV, or plain text) to process_file() and receives normalized records. The module auto-detects the file type by magic bytes and CSV sniffing.

## Tests

Run python3 run_tests.py and python3 run_demo.py.

Dashboard: https://smb-contractor-1099-payment-threshold-tr.vokrix.co
Vercel: smb-contractor-1099-payment-threshold-tr
