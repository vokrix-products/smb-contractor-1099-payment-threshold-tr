import json
import os
import time
import traceback
from datetime import datetime, timezone

import requests

import processor

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
PRODUCT_ID = os.environ.get("PRODUCT_ID", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

JOBS_URL = f"{SUPABASE_URL}/rest/v1/jobs"
RECORDS_URL = f"{SUPABASE_URL}/rest/v1/records"
NOTIFICATIONS_URL = "https://njyvnmczoydsaewvfhyq.supabase.co/rest/v1/notifications"


def get_headers():
    return {
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "apikey": SUPABASE_SERVICE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def download_file(bucket, file_path):
    if file_path.startswith(bucket + "/"):
        file_path = file_path[len(bucket) + 1:]
    url = f"{SUPABASE_URL}/storage/v1/object/{bucket}/{file_path}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {SUPABASE_SERVICE_KEY}", "apikey": SUPABASE_SERVICE_KEY})
    resp.raise_for_status()
    return resp.content


def upload_result(bucket, file_path, content):
    if file_path.startswith(bucket + "/"):
        file_path = file_path[len(bucket) + 1:]
    url = f"{SUPABASE_URL}/storage/v1/object/{bucket}/{file_path}"
    resp = requests.post(url, headers={"Authorization": f"Bearer {SUPABASE_SERVICE_KEY}", "apikey": SUPABASE_SERVICE_KEY, "Content-Type": "application/json"}, data=content)
    resp.raise_for_status()
    return f"{bucket}/{file_path}"


def update_job(job_id, payload):
    url = f"{JOBS_URL}?id=eq.{job_id}"
    resp = requests.patch(url, headers=get_headers(), json=payload)
    resp.raise_for_status()


def insert_notification(customer_id, title, body, notif_type):
    try:
        payload = {
            "product_id": PRODUCT_ID,
            "customer_id": customer_id,
            "title": title,
            "body": body,
            "type": notif_type,
            "read": False,
        }
        resp = requests.post(NOTIFICATIONS_URL, headers=get_headers(), json=payload)
        resp.raise_for_status()
    except Exception:
        traceback.print_exc()


def process_job(job):
    job_id = job["id"]
    customer_id = job.get("customer_id", "")
    input_file_path = job.get("input_file_path", "")
    try:
        bucket = "uploads"
        file_bytes = download_file(bucket, input_file_path)
        records = processor.process_file(file_bytes)

        output_payload = {
            "product_id": PRODUCT_ID,
            "customer_id": customer_id,
            "records": records,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }
        result_json = json.dumps(output_payload).encode("utf-8")
        output_file_path = f"results/{job_id}.json"
        stored_path = upload_result("results", output_file_path, result_json)

        rec_payload = []
        for rec in records:
            rec_payload.append({
                "product_id": PRODUCT_ID,
                "customer_id": customer_id,
                "title": rec.get("title", "Unknown Payee"),
                "status": rec.get("status", "contractor_incomplete_data:warning"),
                "details": rec.get("details", {}),
                "source_file_path": input_file_path,
                "due_date": rec.get("due_date"),
            })
        if rec_payload:
            resp = requests.post(RECORDS_URL, headers=get_headers(), json=rec_payload)
            resp.raise_for_status()

        update_job(job_id, {
            "status": "completed",
            "output_file_path": stored_path,
            "result_summary": f"Processed {len(records)} contractor records.",
            "completed_at": datetime.now(timezone.utc).isoformat(),
        })
        insert_notification(customer_id, "Processing complete", "Your upload has been processed successfully.", "success")
    except Exception as exc:
        traceback.print_exc()
        try:
            update_job(job_id, {
                "status": "failed",
                "result_summary": f"Error: {str(exc)[:500]}",
                "completed_at": datetime.now(timezone.utc).isoformat(),
            })
            insert_notification(customer_id, "Processing failed", "There was an error processing your upload.", "error")
        except Exception:
            traceback.print_exc()


def poll():
    while True:
        try:
            params = {
                "status": "eq.pending",
                "job_type": "eq.process_upload",
                "product_id": f"eq.{PRODUCT_ID}",
                "select": "*",
            }
            resp = requests.get(JOBS_URL, headers=get_headers(), params=params)
            resp.raise_for_status()
            jobs = resp.json()
            for job in jobs:
                process_job(job)
        except Exception:
            traceback.print_exc()
        time.sleep(60)


if __name__ == "__main__":
    print("Poller started")
    poll()
