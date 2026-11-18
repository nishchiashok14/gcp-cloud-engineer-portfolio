
import logging
from datetime import datetime, timezone
from google.cloud import storage

# Configure logging for Cloud Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BUCKET_NAME = "project-04354dfd-b58a-4510-a66-backup"
DESTINATION_NAME = "sample.txt"

def run_backup():
    logging.info("Backup started")

    # Connect to Google Cloud Storage
    client = storage.Client()

    # Select the bucket
    bucket = client.bucket(BUCKET_NAME)

    # Create timestamped sample backup content
    timestamp = datetime.now(timezone.utc).isoformat()
    content = f"GCP automated backup created at {timestamp}\n"

    # Upload the backup
    blob = bucket.blob(DESTINATION_NAME)
    blob.upload_from_string(
        content,
        content_type="text/plain"
    )

    logging.info("Backup uploaded successfully")
    logging.info("Bucket: %s", BUCKET_NAME)
    logging.info("Object: %s", DESTINATION_NAME)

if __name__ == "__main__":
    try:
        run_backup()
    except Exception:
        logging.exception("Backup failed")
        raise
