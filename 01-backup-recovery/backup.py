import logging
from google.cloud import storage

# Configure logging
logging.basicConfig(
    filename="backup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    client = storage.Client()

    BUCKET_NAME = "project-04354dfd-b58a-4510-a66-backup"
    FILE_PATH = "sample.txt"
    DESTINATION_NAME = "sample.txt"

    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(DESTINATION_NAME)

    logging.info("Backup started")

    blob.upload_from_filename(FILE_PATH)

    logging.info("Backup uploaded successfully")
    print("Backup uploaded successfully!")

except Exception as error:
    logging.exception("Backup failed")
    print("Backup failed:", error)
